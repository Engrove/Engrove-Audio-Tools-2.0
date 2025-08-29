// scripts/vuemap/generate-ssm.mjs
// v4.0
// === SYFTE & ANSVAR ===
// Detta Node.js-skript genererar en System Semantic Map (SSM) i JSON-format.
// Det använder industristandardverktyg för att tillförlitligt parsa modern
// Vue 3- och JavaScript-syntax (ES2020+).
// === HISTORIK ===
// v3.0 - v3.5: Se tidigare versioner.
// v3.6: Egen generisk AST-traverser. Robust hantering av getters/actions.
// v4.0: KRITISK UPPGRADERING. Infört djupgående analys av Vue-komponenter
//       (<script> och <template>) samt Vue Router. Mappar nu props, emits,
//       komponentanvändning, store-beroenden och rutter för en fullständig
//       semantisk systemgraf.

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';
import vueEslintParser from 'vue-eslint-parser';
import * as tsParser from '@typescript-eslint/parser';

const { parseForESLint } = vueEslintParser;

// --- Hjälp: generisk AST-traverser (DFS) ---
function traverse(node, { enter }, parent = null) {
  if (!node || typeof node !== 'object') return;
  if (node.type) enter(node, parent);
  for (const key of Object.keys(node)) {
    const child = node[key];
    if (!child) continue;
    if (Array.isArray(child)) {
      for (const c of child) traverse(c, { enter }, node);
    } else if (typeof child === 'object' && child.type) {
      traverse(child, { enter }, node);
    }
  }
}

// --- Kärnfunktioner ---
async function calculateSha256(filepath) {
  const fileBuffer = await fs.readFile(filepath);
  return crypto.createHash('sha256').update(fileBuffer).digest('hex');
}

function isBinary(filepath) {
  const binaryExtensions = ['.webp', '.jpg', '.jpeg', '.gif', '.png', '.pdf'];
  return binaryExtensions.some(ext => filepath.toLowerCase().endsWith(ext));
}

function determineFileType(filepath) {
  const lower = filepath.toLowerCase();
  if (filepath.endsWith('.vue')) return 'VueComponent';
  if (filepath.endsWith('.js') || filepath.endsWith('.mjs') || filepath.endsWith('.ts')) {
    if (lower.includes('store')) return 'PiniaStore';
    if (lower.includes('router')) return 'RouterConfig';
    if (lower.includes('main.js')) return 'EntryPoint';
    return 'Utility';
  }
  if (filepath.endsWith('.json')) return 'StaticData';
  if (isBinary(filepath)) return 'BinaryAsset';
  return 'Other';
}

async function createFileNode(filepath, rootDir) {
  const relativePath = path.relative(rootDir, filepath).replace(/\\/g, '/');
  const fileType = determineFileType(filepath);
  return {
    id: relativePath,
    type: 'File',
    path: relativePath,
    hash: await calculateSha256(filepath),
    fileType,
    purpose: `Represents the file artifact at ${relativePath}.`
  };
}

// --- AST Analys & Berikning ---
function getIdentifierName(node) {
    if (!node) return undefined;
    if (node.type === 'Identifier') return node.name;
    if (node.type === 'Literal') return String(node.value);
    if (node.type === 'TemplateLiteral' && node.quasis.length === 1) return node.quasis[0].value.raw;
    return undefined;
}

function safePropName(prop) {
  if (!prop) return undefined;
  return getIdentifierName(prop.key);
}

function analyzeVueComponent(ast, fileId, rootDir) {
    const nodes = [];
    const edges = [];
    const componentId = fileId;
    const scriptAst = ast.services.getScriptAST();
    const imports = new Map();

    // 1. Analysera <script> först för att samla in beroenden
    traverse(scriptAst, {
        enter(node) {
            // Samla imports för att kunna mappa komponentnamn till sökvägar
            if (node.type === 'ImportDeclaration' && node.source.value) {
                const sourcePath = node.source.value;
                for (const specifier of node.specifiers) {
                    if (specifier.type === 'ImportDefaultSpecifier' || specifier.type === 'ImportSpecifier') {
                        imports.set(specifier.local.name, sourcePath);
                    }
                }
            }
            // defineProps, defineEmits
            if (node.type === 'CallExpression' && ['defineProps', 'defineEmits'].includes(node.callee.name)) {
                const type = node.callee.name === 'defineProps' ? 'Prop' : 'Event';
                const edgeType = node.callee.name === 'defineProps' ? 'DEFINES_PROP' : 'DEFINES_EVENT';
                const arg = node.arguments[0];
                let items = [];

                if (arg?.type === 'ArrayExpression') {
                    items = arg.elements.map(el => getIdentifierName(el)).filter(Boolean);
                } else if (arg?.type === 'ObjectExpression') {
                    items = arg.properties.map(p => safePropName(p)).filter(Boolean);
                }

                for (const itemName of items) {
                    const nodeId = `${componentId}#${type.toLowerCase()}.${itemName}`;
                    nodes.push({ id: nodeId, type, path: fileId, parent: componentId, name: itemName });
                    edges.push({ source: componentId, target: nodeId, type: edgeType });
                }
            }
            // useStore anrop
            if (node.type === 'CallExpression' && node.callee.name?.startsWith('use') && node.callee.name?.endsWith('Store')) {
                const storeImportPath = imports.get(node.callee.name);
                if (storeImportPath) {
                    const resolvedPath = path.relative(rootDir, path.resolve(path.dirname(path.join(rootDir, fileId)), storeImportPath)).replace(/\\/g, '/');
                    edges.push({ source: componentId, target: resolvedPath, type: 'USES_STORE_FILE' });
                }
            }
        }
    });
    
    // 2. Analysera <template>
    const templateAst = ast.templateBody;
    if (templateAst) {
        traverse(templateAst, {
            enter(node) {
                if (node.type === 'VElement') {
                    const tagName = node.name;
                    // Mappa tagg till importerad komponent
                    if (imports.has(tagName)) {
                        const componentImportPath = imports.get(tagName);
                        const resolvedPath = path.relative(rootDir, path.resolve(path.dirname(path.join(rootDir, fileId)), componentImportPath)).replace(/\\/g, '/');
                        edges.push({ source: componentId, target: resolvedPath, type: 'USES_COMPONENT' });
                    }
                }
            }
        });
    }

    return { nodes, edges };
}

function analyzePiniaStore(ast, fileId) {
  // ... (befintlig kod för analyzePiniaStore är oförändrad) ...
  const storeNodes = [];
  const storeEdges = [];

  traverse(ast, {
    enter(node) {
      if (node.type === 'CallExpression' && node.callee?.name === 'defineStore') {
        let storeId = 'unknown';
        if (node.arguments?.length) {
          const a0 = node.arguments[0];
          if (a0?.type === 'Literal' && (typeof a0.value === 'string' || typeof a0.value === 'number')) {
            storeId = String(a0.value);
          } else if (a0?.type === 'Identifier') {
            storeId = a0.name;
          }
        }

        const mainStoreNode = { id: storeId, type: 'Store', path: fileId, storeId, purpose: `Manages state for the '${storeId}' domain.` };
        storeNodes.push(mainStoreNode);
        edges.push({ source: fileId, target: storeId, type: 'DEFINES' });

        const storeDef = node.arguments?.[1];
        if (storeDef?.type === 'ObjectExpression') {
          const props = storeDef.properties || [];
          const stateProp = props.find(p => safePropName(p) === 'state');
          let stateObj = null;
          if (stateProp?.value?.type === 'ArrowFunctionExpression' || stateProp?.value?.type === 'FunctionExpression') {
            const body = stateProp.value.body;
            if (body?.type === 'BlockStatement') {
              const ret = body.body?.find(n => n.type === 'ReturnStatement');
              if (ret?.argument?.type === 'ObjectExpression') stateObj = ret.argument;
            } else if (body?.type === 'ObjectExpression') {
              stateObj = body;
            }
          }
          if (stateObj?.type === 'ObjectExpression') {
            for (const prop of stateObj.properties || []) {
              const keyName = safePropName(prop);
              if (!keyName) continue;
              const stateNodeId = `${storeId}#state.${keyName}`;
              storeNodes.push({ id: stateNodeId, type: 'StateVariable', path: fileId, parent: storeId, dataType: 'Unknown', purpose: `Represents the '${keyName}' state property.` });
              storeEdges.push({ source: storeId, target: stateNodeId, type: 'DEFINES' });
            }
          }
          for (const section of ['getters', 'actions']) {
            const sectionProp = props.find(p => safePropName(p) === section);
            if (sectionProp?.value?.type === 'ObjectExpression') {
              for (const prop of sectionProp.value.properties || []) {
                const name = safePropName(prop);
                if (!name) continue;
                const propType = section === 'getters' ? 'Getter' : 'Action';
                const propId = `${storeId}#${section}.${name}`;
                storeNodes.push({ id: propId, type: propType, path: fileId, parent: storeId, purpose: `A ${section.slice(0, -1)} for the '${storeId}' store.` });
                storeEdges.push({ source: storeId, target: propId, type: 'DEFINES' });
                const v = prop.value;
                let body = null;
                if (v?.type === 'FunctionExpression' || v?.type === 'ArrowFunctionExpression') {
                  body = v.body;
                } else if (v?.type === 'Property' && (v.value?.type === 'FunctionExpression' || v.value?.type === 'ArrowFunctionExpression')) {
                  body = v.value.body;
                }
                if (!body) continue;
                const bodyNode = body;
                traverse(bodyNode, {
                  enter(childNode, parentNode) {
                    if (childNode.type === 'MemberExpression' && childNode.object?.type === 'ThisExpression') {
                      const propertyName = childNode.property?.name || childNode.property?.value;
                      if (!propertyName) return;
                      const stateId = `${storeId}#state.${propertyName}`;
                      if (parentNode?.type === 'AssignmentExpression' && parentNode.left === childNode) {
                        storeEdges.push({ source: propId, target: stateId, type: 'MODIFIES_STATE' });
                      } else {
                        storeEdges.push({ source: propId, target: stateId, type: 'READS_STATE' });
                      }
                    }
                    if (childNode.type === 'CallExpression' && childNode.callee?.type === 'MemberExpression' && childNode.callee.object?.type === 'ThisExpression') {
                      const calleeName = childNode.callee.property?.name || childNode.callee.property?.value;
                      if (!calleeName) return;
                      const targetId = `${storeId}#actions.${calleeName}`;
                      if (targetId !== propId) {
                        storeEdges.push({ source: propId, target: targetId, type: 'CALLS' });
                      }
                    }
                  }
                });
              }
            }
          }
        }
      }
    }
  });
  return { nodes: storeNodes, edges: storeEdges };
}

function analyzeRouter(ast, fileId, rootDir) {
    const nodes = [];
    const edges = [];

    traverse(ast, {
        enter(node) {
            if (node.type === 'VariableDeclarator' && node.id.name === 'routes' && node.init.type === 'ArrayExpression') {
                for (const routeObject of node.init.elements) {
                    if (routeObject.type !== 'ObjectExpression') continue;

                    let routePath = 'N/A', routeName = 'N/A', componentImport = 'N/A';
                    
                    routeObject.properties.forEach(prop => {
                        const key = safePropName(prop);
                        if (key === 'path' && prop.value.type === 'Literal') routePath = prop.value.value;
                        if (key === 'name' && prop.value.type === 'Literal') routeName = prop.value.value;
                        if (key === 'component' && prop.value.type === 'ArrowFunctionExpression' && prop.value.body.type === 'ImportExpression') {
                            componentImport = prop.value.body.source.value;
                        }
                    });

                    if (routePath !== 'N/A' && componentImport !== 'N/A') {
                        const routeId = `route:${routePath}`;
                        nodes.push({ id: routeId, type: 'Route', path: fileId, routePath, routeName, purpose: `Defines the '${routeName}' route at '${routePath}'.` });
                        
                        const resolvedPath = path.relative(rootDir, path.resolve(path.dirname(path.join(rootDir, fileId)), componentImport)).replace(/\\/g, '/');
                        edges.push({ source: routeId, target: resolvedPath, type: 'RENDERS_COMPONENT' });
                        edges.push({ source: fileId, target: routeId, type: 'DEFINES_ROUTE' });
                    }
                }
            }
        }
    });
    return { nodes, edges };
}

// --- Huvudlogik ---
async function main(rootDir, outputFile) {
  console.log('Startar generering av System Semantic Map (SSM)...');

  const allNodes = [];
  const allEdges = [];

  const targetPatterns = ['src/**/*.{js,ts,vue,json,css}', 'public/data/**/*.{json,webp}'];
  const files = await glob(targetPatterns, { cwd: rootDir, nodir: true });

  console.log(`  - Hittade ${files.length} relevanta filer...`);

  for (const relativePath of files.map(f => f.replace(/\\/g, '/'))) {
    const filepath = path.join(rootDir, relativePath);

    const fileNode = await createFileNode(filepath, rootDir);
    allNodes.push(fileNode);

    if (isBinary(filepath) || filepath.endsWith('.json') || filepath.endsWith('.css')) continue;

    try {
      const content = await fs.readFile(filepath, 'utf-8');
      const parsed = parseForESLint(content, {
        filePath: filepath,
        parser: tsParser,
        sourceType: 'module',
        ecmaVersion: 'latest',
        parserOptions: {
            templateTokenizer: { patch: true }
        }
      });
      const ast = parsed.ast;

      // Import edges
      if (ast?.body) {
        for (const node of ast.body) {
          if (node.type === 'ImportDeclaration' && node.source?.value) {
            const sourcePath = node.source.value;
            if (typeof sourcePath === 'string') {
                const resolvedTarget = path.relative(rootDir, path.resolve(path.dirname(filepath), sourcePath)).replace(/\\/g, '/');
                allEdges.push({ source: relativePath, target: resolvedTarget, type: 'IMPORTS' });
            }
          }
        }
      }

      // Filtypsspecifik analys
      if (fileNode.fileType === 'PiniaStore') {
        const { nodes, edges } = analyzePiniaStore(ast, relativePath);
        allNodes.push(...nodes);
        allEdges.push(...edges);
      } else if (fileNode.fileType === 'VueComponent') {
        const { nodes, edges } = analyzeVueComponent(parsed, relativePath, rootDir);
        allNodes.push(...nodes);
        allEdges.push(...edges);
      } else if (fileNode.fileType === 'RouterConfig') {
        const { nodes, edges } = analyzeRouter(ast, relativePath, rootDir);
        allNodes.push(...nodes);
        allEdges.push(...edges);
      }
    } catch (e) {
      console.warn(`    - Varning: Kunde inte parsa ${relativePath}: ${e.message}`);
      allEdges.push({
        source: relativePath,
        target: 'PARSING_ERROR',
        type: 'HAS_ERROR',
        details: e.message
      });
    }
  }

  const ssm = {
    "$schema": "./system_semantic_map.schema.json",
    "version": "4.0.0",
    "createdAt": new Date().toISOString(),
    "nodes": allNodes,
    "edges": allEdges
  };

  const outputPath = path.join(rootDir, outputFile);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(ssm, null, 2));

  console.log(`\nSSM genererad framgångsrikt!`);
  console.log(`  - Noder: ${allNodes.length}`);
  console.log(`  - Kanter: ${allEdges.length}`);
  console.log(`  - Output: ${outputFile}`);
}

const rootDir = process.argv[2] || '.';
const outputFile = process.argv[3] || 'scripts/vuemap/system_semantic_map.json';
main(rootDir, outputFile).catch(err => {
  console.error(err);
  process.exitCode = 1;
});
