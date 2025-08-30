// scripts/vuemap/generate-ssm.mjs
// v5.0
// Ändringar v5.0:
// - PROTOKOLL-TRANSFORMATION: Genererar nu en fullständig, exekverbar protokollfil (P-SAAP-1.0).
// - ARKITEKTURREGLER: Innehåller nu definitioner för arkitektoniska lager, placeringsregler och beroenderegler.
// - AKTIV VALIDERING: Validerar aktivt filstrukturen och importer mot de definierade reglerna under körning.
// - RAPPORTERING: Lägger till en `violations`-sektion i outputen för att rapportera alla upptäckta arkitektoniska avvikelser.
// - Behåller v4.5-fixar.

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';
import vueEslintParser from 'vue-eslint-parser';
import * as tsParser from '@typescript-eslint/parser';

const { parseForESLint } = vueEslintParser;

// --- DEFINITION AV ARKITEKTURREGLER (Protokollets Kärna) ---

const ARCHITECTURAL_LAYERS = [
  { layer: 0, name: "shared", pathPrefix: "src/shared" },
  { layer: 1, name: "entities", pathPrefix: "src/entities" },
  { layer: 2, name: "features", pathPrefix: "src/features" },
  { layer: 3, name: "widgets", pathPrefix: "src/widgets" },
  { layer: 4, name: "pages", pathPrefix: "src/pages" },
  { layer: 5, name: "app", pathPrefix: "src/app" },
];

const PLACEMENT_RULES = [
  { fileType: "VueComponent", purpose: "UI Primitive", allowedPath: /^src\/shared\/ui\/.*\.vue$/ },
  { fileType: "PiniaStore", purpose: "Business Entity State", allowedPath: /^src\/entities\/[a-zA-Z0-9-]+\/model\/.*\.js$/ },
  { fileType: "VueComponent", purpose: "Feature Implementation", allowedPath: /^src\/features\/[a-zA-Z0-9-]+\/ui\/.*\.vue$/ },
  { fileType: "VueComponent", purpose: "Page Layout", allowedPath: /^src\/pages\/[a-zA-Z0-9-]+\/.*\.vue$/ },
  { fileType: "RouterConfig", purpose: "Application Routing", allowedPath: /^src\/app\/router\.js$/ },
  { fileType: "EntryPoint", purpose: "Application Entry Point", allowedPath: /^src\/app\/main\.js$/ },
];

const DEPENDENCY_RULES = {
  "app": ["pages", "widgets", "features", "entities", "shared"],
  "pages": ["widgets", "features", "entities", "shared"],
  "widgets": ["features", "entities", "shared"],
  "features": ["entities", "shared"],
  "entities": ["shared"],
  "shared": ["shared"],
};


// --- Hjälp: cykelsäker AST-traverser (DFS) ---
function traverse(root, { enter }) {
  const seen = new WeakSet();
  const SKIP_KEYS = new Set(['parent', 'tokens', 'comments', 'loc', 'range']);

  function walk(node, parent = null) {
    if (!node || typeof node !== 'object') return;
    if (seen.has(node)) return;
    seen.add(node);

    if (node.type) enter(node, parent);

    for (const key of Object.keys(node)) {
      if (SKIP_KEYS.has(key)) continue;
      const child = node[key];
      if (!child) continue;

      if (Array.isArray(child)) {
        for (const c of child) {
          if (c && typeof c === 'object') walk(c, node);
        }
      } else if (typeof child === 'object' && child.type) {
        walk(child, node);
      }
    }
  }

  walk(root, null);
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
  if (filepath.endsWith('.css')) return 'StyleSheet';
  if (filepath.endsWith('.js') || filepath.endsWith('.mjs') || filepath.endsWith('.ts')) {
    if (lower.includes('/model/') && (lower.endsWith('store.js') || lower.endsWith('store.ts'))) return 'PiniaStore';
    if (lower.includes('/app/router')) return 'RouterConfig';
    if (lower.includes('/app/main')) return 'EntryPoint';
    return 'Utility';
  }
  if (filepath.endsWith('.json')) return 'StaticData';
  if (isBinary(filepath)) return 'BinaryAsset';
  return 'Other';
}

function determinePurpose(fileNode) {
    if (fileNode.fileType === 'VueComponent') {
        if (fileNode.path.startsWith('src/shared/ui/')) return 'UI Primitive';
        if (fileNode.path.startsWith('src/features/')) return 'Feature Implementation';
        if (fileNode.path.startsWith('src/pages/')) return 'Page Layout';
    }
    if (fileNode.fileType === 'PiniaStore') return 'Business Entity State';
    if (fileNode.fileType === 'RouterConfig') return 'Application Routing';
    if (fileNode.fileType === 'EntryPoint') return 'Application Entry Point';
    return `Represents the file artifact at ${fileNode.path}.`;
}

async function createFileNode(filepath, rootDir) {
  const relativePath = path.relative(rootDir, filepath).replace(/\\/g, '/');
  const fileNode = {
    id: relativePath,
    type: 'File',
    path: relativePath,
    hash: await calculateSha256(filepath),
    fileType: determineFileType(filepath),
    purpose: '' // Placeholder
  };
  fileNode.purpose = determinePurpose(fileNode);
  return fileNode;
}

// --- AST-verktyg ---
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

// --- Arkitekturvalidering ---
function getLayer(filePath) {
    const layer = ARCHITECTURAL_LAYERS.find(l => filePath.startsWith(l.pathPrefix));
    return layer ? layer : null;
}

function validatePlacement(fileNode) {
    const applicableRule = PLACEMENT_RULES.find(r => r.fileType === fileNode.fileType && (r.purpose ? r.purpose === fileNode.purpose : true));
    if (applicableRule && !applicableRule.allowedPath.test(fileNode.path)) {
        return {
            type: 'PLACEMENT_VIOLATION',
            source: fileNode.path,
            details: `File of type '${fileNode.fileType}' with purpose '${fileNode.purpose}' is misplaced. Expected location matching: ${applicableRule.allowedPath.toString()}`
        };
    }
    return null;
}

function validateDependency(edge, fileNodes) {
    if (edge.type !== 'IMPORTS' || !edge.target.endsWith('.js') && !edge.target.endsWith('.vue')) {
        return null; // Validera bara interna JS/Vue-importer
    }

    const sourceLayer = getLayer(edge.source);
    const targetLayer = getLayer(edge.target);

    if (!sourceLayer || !targetLayer) {
        return null; // Kan inte validera om en fil inte tillhör ett lager
    }

    if (sourceLayer.layer < targetLayer.layer) {
        return {
            type: 'DEPENDENCY_VIOLATION',
            source: edge.source,
            target: edge.target,
            details: `Illegal import from lower layer '${sourceLayer.name}' (L${sourceLayer.layer}) to higher layer '${targetLayer.name}' (L${targetLayer.layer}).`
        };
    }
    
    const allowedImports = DEPENDENCY_RULES[sourceLayer.name] || [];
    if (!allowedImports.includes(targetLayer.name)) {
         return {
            type: 'DEPENDENCY_VIOLATION',
            source: edge.source,
            target: edge.target,
            details: `Layer '${sourceLayer.name}' is not allowed to import from layer '${targetLayer.name}'. Allowed: [${allowedImports.join(', ')}]`
        };
    }

    return null;
}


// --- Specifik filanalys (Vue, Pinia, Router) ---
// (Funktionerna analyzeVueComponent, analyzePiniaStore, analyzeRouter förblir i stort sett oförändrade från v4.5)
function analyzeVueComponent(parsed, fileId, rootDir) {
  const nodes = [];
  const edges = [];
  const componentId = fileId;

  const programAst = parsed?.ast;
  const imports = new Map();

  if (programAst) {
    traverse(programAst, {
      enter(node) {
        // Imports
        if (node.type === 'ImportDeclaration' && node.source?.value) {
          const sourcePath = node.source.value;
          for (const specifier of node.specifiers || []) {
            if (specifier.type === 'ImportDefaultSpecifier' || specifier.type === 'ImportSpecifier') {
              imports.set(specifier.local.name, sourcePath);
            }
          }
        }
        // defineProps / defineEmits
        if (node.type === 'CallExpression' && ['defineProps', 'defineEmits'].includes(node.callee?.name)) {
          const type = node.callee.name === 'defineProps' ? 'Prop' : 'Event';
          const edgeType = node.callee.name === 'defineProps' ? 'DEFINES_PROP' : 'DEFINES_EVENT';
          const arg = node.arguments?.[0];
          let items = [];

          if (arg?.type === 'ArrayExpression') {
            items = (arg.elements || []).map(el => getIdentifierName(el)).filter(Boolean);
          } else if (arg?.type === 'ObjectExpression') {
            items = (arg.properties || []).map(p => safePropName(p)).filter(Boolean);
          }

          for (const itemName of items) {
            const nodeId = `${componentId}#${type.toLowerCase()}.${itemName}`;
            nodes.push({ id: nodeId, type, path: fileId, parent: componentId, name: itemName });
            edges.push({ source: componentId, target: nodeId, type: edgeType });
          }
        }

        // useXStore()
        if (node.type === 'CallExpression' && node.callee?.name?.startsWith('use') && node.callee?.name?.endsWith('Store')) {
          const storeImportPath = imports.get(node.callee.name);
          if (storeImportPath) {
            let resolvedPath;
            if (storeImportPath.startsWith('@/')) {
                 resolvedPath = storeImportPath.replace('@/', 'src/');
            } else {
                 resolvedPath = path
                .relative(rootDir, path.resolve(path.dirname(path.join(rootDir, fileId)), storeImportPath))
                .replace(/\\/g, '/');
            }
            edges.push({ source: componentId, target: resolvedPath, type: 'USES_STORE_FILE' });
          }
        }
      }
    });
  }

  // <template>-del (via vue-eslint-parser -> templateBody)
  const templateAst = programAst?.templateBody;
  if (templateAst) {
    traverse(templateAst, {
      enter(node) {
        if (node.type === 'VElement') {
          const tagName = node.name;
          // Korrigering för att matcha komponentnamn som 'Logo' med importnamn
          const importedName = Array.from(imports.keys()).find(key => key.toLowerCase() === tagName.toLowerCase());
          if (importedName && imports.has(importedName)) {
            const componentImportPath = imports.get(importedName);
            let resolvedPath;
             if (componentImportPath.startsWith('@/')) {
                 resolvedPath = componentImportPath.replace('@/', 'src/');
            } else {
                 resolvedPath = path
                .relative(rootDir, path.resolve(path.dirname(path.join(rootDir, fileId)), componentImportPath))
                .replace(/\\/g, '/');
            }
            edges.push({ source: componentId, target: resolvedPath, type: 'USES_COMPONENT' });
          }
        }
      }
    });
  }

  return { nodes, edges };
}
function analyzePiniaStore(ast, fileId) {
  const storeNodes = [];
  const storeEdges = [];

  traverse(ast, {
    enter(node, parent) {
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

        const mainStoreNode = {
          id: storeId,
          type: 'Store',
          path: fileId,
          storeId,
          purpose: `Manages state for the '${storeId}' domain.`
        };
        storeNodes.push(mainStoreNode);
        storeEdges.push({ source: fileId, target: storeId, type: 'DEFINES' });

        const storeDef = node.arguments?.[1];
        if (storeDef?.type === 'ObjectExpression') {
          const props = storeDef.properties || [];

          // state
          const stateProp = props.find(p => safePropName(p) === 'state');
          let stateObj = null;
          if (stateProp?.value?.type === 'ArrowFunctionExpression' || stateProp?.value?.type === 'FunctionExpression') {
            const body = stateProp.value.body;
            if (body?.type === 'BlockStatement') {
              const ret = (body.body || []).find(n => n.type === 'ReturnStatement');
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
              storeNodes.push({
                id: stateNodeId,
                type: 'StateVariable',
                path: fileId,
                parent: storeId,
                dataType: 'Unknown',
                purpose: `Represents the '${keyName}' state property.`
              });
              storeEdges.push({ source: storeId, target: stateNodeId, type: 'DEFINES' });
            }
          }

          // getters / actions
          for (const section of ['getters', 'actions']) {
            const sectionProp = props.find(p => safePropName(p) === section);
            if (sectionProp?.value?.type === 'ObjectExpression') {
              for (const prop of sectionProp.value.properties || []) {
                const name = safePropName(prop);
                if (!name) continue;
                const propType = section === 'getters' ? 'Getter' : 'Action';
                const propId = `${storeId}#${section}.${name}`;
                storeNodes.push({
                  id: propId,
                  type: propType,
                  path: fileId,
                  parent: storeId,
                  purpose: `A ${section.slice(0, -1)} for the '${storeId}' store.`
                });
                storeEdges.push({ source: storeId, target: propId, type: 'DEFINES' });

                const v = prop.value;
                let body = null;
                if (v?.type === 'FunctionExpression' || v?.type === 'ArrowFunctionExpression') {
                  body = v.body;
                } else if (v?.type === 'Property' && (v.value?.type === 'FunctionExpression' || v.value?.type === 'ArrowFunctionExpression')) {
                  body = v.value.body;
                }
                if (!body) continue;

                traverse(body, {
                  enter(childNode, parentNode) {
                    // this.x läs/skriv
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
                    // this.action()
                    if (
                      childNode.type === 'CallExpression' &&
                      childNode.callee?.type === 'MemberExpression' &&
                      childNode.callee.object?.type === 'ThisExpression'
                    ) {
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
  const imports = new Map();

  // Steg 1: Samla alla top-level importer
  traverse(ast, {
    enter(node) {
      if (node.type === 'ImportDeclaration' && node.source?.value) {
        const sourcePath = node.source.value;
        for (const specifier of node.specifiers || []) {
          if (specifier.type === 'ImportDefaultSpecifier') {
            imports.set(specifier.local.name, sourcePath);
          }
        }
      }
    }
  });

  // Steg 2: Hitta och analysera routes-arrayen
  traverse(ast, {
    enter(node) {
      if (node.type === 'VariableDeclarator' && node.id?.name === 'routes' && node.init?.type === 'ArrayExpression') {
        for (const routeObject of node.init.elements || []) {
          if (routeObject?.type !== 'ObjectExpression') continue;

          let routePath = 'N/A', routeName = 'N/A', componentImportPath = null;
          
          let componentIdentifierName = null;

          (routeObject.properties || []).forEach(prop => {
            const key = safePropName(prop);
            if (key === 'path' && prop.value?.type === 'Literal') routePath = prop.value.value;
            if (key === 'name' && prop.value?.type === 'Literal') routeName = prop.value.value;

            // Hantera statisk import (component: HomePage)
            if (key === 'component' && prop.value?.type === 'Identifier') {
                componentIdentifierName = prop.value.name;
            }
            // Hantera dynamisk import (component: () => import(...))
            if (
              key === 'component' &&
              prop.value?.type === 'ArrowFunctionExpression' &&
              prop.value.body?.type === 'ImportExpression'
            ) {
              componentImportPath = prop.value.body.source?.value;
            }
          });

          // Lös upp sökvägen baserat på typ av import
          if (componentIdentifierName && imports.has(componentIdentifierName)) {
            componentImportPath = imports.get(componentIdentifierName);
          }
          
          if (routePath !== 'N/A' && componentImportPath) {
            const routeId = `route:${routePath}`;
            nodes.push({
              id: routeId,
              type: 'Route',
              path: fileId,
              routePath,
              routeName,
              purpose: `Defines the '${routeName}' route at '${routePath}'.`
            });

            const resolvedPath = path
              .relative(rootDir, path.resolve(path.dirname(path.join(rootDir, fileId)), componentImportPath))
              .replace(/\\/g, '/');
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
  console.log('Startar generering av System Architecture Adherence Protocol (SAAP)...');

  const allNodes = [];
  const allEdges = [];
  const allViolations = [];

  const targetPatterns = ['src/**/*.{js,ts,vue,json,css}', 'public/data/**/*.{json,webp}'];
  const files = await glob(targetPatterns, { cwd: rootDir, nodir: true });

  console.log(`  - Hittade ${files.length} relevanta filer...`);

  // Steg 1: Skapa alla filnoder och validera placering
  for (const relativePath of files.map(f => f.replace(/\\/g, '/'))) {
    const filepath = path.join(rootDir, relativePath);
    const fileNode = await createFileNode(filepath, rootDir);
    allNodes.push(fileNode);

    const placementViolation = validatePlacement(fileNode);
    if (placementViolation) {
        allViolations.push(placementViolation);
    }
  }

  // Steg 2: Parsa filer och generera kanter
  for (const fileNode of allNodes.filter(n => n.type === 'File')) {
    const { path: relativePath } = fileNode;
    const filepath = path.join(rootDir, relativePath);

    if (isBinary(filepath) || filepath.endsWith('.json') || filepath.endsWith('.css')) continue;

    try {
      const content = await fs.readFile(filepath, 'utf-8');
      let parsed;
      try {
        parsed = parseForESLint(content, { filePath, parser: tsParser, sourceType: 'module', ecmaVersion: 'latest' });
      } catch (err) {
        parsed = { ast: tsParser.parse(content, { sourceType: 'module', ecmaVersion: 'latest' }) };
      }
      const ast = parsed.ast;

      // Import-edges
      if (ast?.body) {
        for (const node of ast.body) {
          if (node.type === 'ImportDeclaration' && node.source?.value) {
            const sourcePath = node.source.value;
            if (typeof sourcePath !== 'string') continue;
            
            if (sourcePath.startsWith('.')) {
              const resolvedTarget = path.join(path.dirname(relativePath), sourcePath).replace(/\\/g, '/');
              const finalTarget = path.normalize(resolvedTarget);
              allEdges.push({ source: relativePath, target: finalTarget, type: 'IMPORTS' });
            } else if (sourcePath.startsWith('@/')) {
              const resolvedTarget = sourcePath.replace('@/', 'src/');
              allEdges.push({ source: relativePath, target: resolvedTarget, type: 'IMPORTS' });
            } else {
              allEdges.push({ source: relativePath, target: sourcePath, type: 'IMPORTS_PACKAGE' });
              if (!allNodes.some(n => n.id === sourcePath && n.type === 'NpmPackage')) {
                allNodes.push({ id: sourcePath, type: 'NpmPackage', name: sourcePath, purpose: `Represents the external NPM dependency '${sourcePath}'.` });
              }
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
      allViolations.push({
        type: 'PARSING_ERROR',
        source: relativePath,
        details: e.message
      });
    }
  }
  
  // Steg 3: Validera beroenden nu när alla kanter är skapade
  console.log('  - Validerar arkitekturregler...');
  for (const edge of allEdges) {
      const dependencyViolation = validateDependency(edge, allNodes);
      if (dependencyViolation) {
          allViolations.push(dependencyViolation);
      }
  }


  const ssm = {
    "$schema": "./system_semantic_map.schema.json",
    "protocolId": "P-SAAP-1.0",
    "title": "System Architecture Adherence Protocol",
    "version": "1.0.0",
    "strict_mode": true,
    "mode": "literal",
    "createdAt": new Date().toISOString(),
    "_comment_layers": "Defines the strict architectural hierarchy. Higher layers can import from lower layers, but not vice versa.",
    "architecturalLayers": ARCHITECTURAL_LAYERS,
    "_comment_placement": "Defines where files MUST be placed based on their type and purpose.",
    "placementRules": PLACEMENT_RULES.map(r => ({...r, allowedPath: r.allowedPath.toString()})), // Konvertera RegExp till strängar för JSON
    "_comment_dependencies": "Defines the legal import paths between layers.",
    "dependencyRules": DEPENDENCY_RULES,
    "_comment_violations": "A log of all detected architectural violations.",
    "violations": allViolations,
    "_comment_nodes": "The node registry for context and artifact identification.",
    "nodes": allNodes,
    "_comment_edges": "The edge registry, superseded by 'dependencyRules' for validation.",
    "edges": allEdges
  };

  const outputPath = path.join(rootDir, outputFile);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(ssm, null, 2));

  console.log(`\nSAAP-protokoll genererat framgångsrikt!`);
  console.log(`  - Noder: ${allNodes.length}`);
  console.log(`  - Kanter: ${allEdges.length}`);
  console.log(`  - Avvikelser: ${allViolations.length}`);
  console.log(`  - Output: ${outputFile}`);
}

const rootDir = process.argv[2] || '.';
const outputFile = process.argv[3] || 'scripts/vuemap/system_semantic_map.json';
main(rootDir, outputFile).catch(err => {
  console.error(err);
  process.exitCode = 1;
});
