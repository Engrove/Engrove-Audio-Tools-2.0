// scripts/vuemap/generate-ssm.mjs
// v4.7
// Förändringslogg:
// - NYTT: Datadriven lagerdetektion via SAAP (layerPathPattern) ersätter hårdkodad logik.
// - NYTT: CLI-flagga --INIT som materialiserar saap.protocol.json från defaultSAAP().
// - NYTT: Förbättrade felmeddelanden för DEPENDENCY med hint om tillåtna mål.
// - NYTT: Hash-baserad cache: återanvänder noder/kanter för oförändrade filer från tidigare SSM.
// - BIBEHÅLLER: v4.6-parsning av Vue, Pinia, Router; alias- och relativ-resolving; STRICT/REPORT-lägen.
// - UTÖKAT: SAAP default inkluderar layerPathPattern per lager.
//
// Beroenden: vue-eslint-parser, @typescript-eslint/parser, glob, minimatch
// Node: ES-modul (.mjs), top-level await tillåtet.

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';
import { minimatch } from 'minimatch';
import vueEslintParser from 'vue-eslint-parser';
import * as tsParser from '@typescript-eslint/parser';

const { parseForESLint } = vueEslintParser;
let CURRENT_SAAP = null;

// -------------------------------------------------------------
// Hjälp: cykelsäker AST-traverser (DFS)
// -------------------------------------------------------------
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

// -------------------------------------------------------------
// Kärnfunktioner
// -------------------------------------------------------------
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
    if (lower.includes('store')) return 'PiniaStore';
    if (lower.includes('router')) return 'RouterConfig';
    if (lower.endsWith('/main.js') || filepath.endsWith('main.js')) return 'EntryPoint';
    return 'Utility';
  }
  if (filepath.endsWith('.json')) return 'StaticData';
  if (isBinary(filepath)) return 'BinaryAsset';
  return 'Other';
}

function detectLayer(relativePath) {
  const p = relativePath.replace(/\\/g, '/');
  if (p.startsWith('public/')) return 'public';
  if (!CURRENT_SAAP || !Array.isArray(CURRENT_SAAP.architecturalLayers)) {
    return p.startsWith('src/') ? 'src-other' : 'external';
  }
  for (const layer of CURRENT_SAAP.architecturalLayers) {
    const name = layer.name;
    const pattern = layer.layerPathPattern || `src/${name}/**/*`;
    if (minimatch(p, pattern, { dot: true })) return name;
    if (name === 'app' && (p === 'src/app/router.js' || p === 'src/app/main.js')) return 'app';
  }
  return p.startsWith('src/') ? 'src-other' : 'external';
}

async function createFileNode(filepath, rootDir) {
  const relativePath = path.relative(rootDir, filepath).replace(/\\/g, '/');
  const fileType = determineFileType(relativePath);
  return {
    id: relativePath,
    type: 'File',
    path: relativePath,
    hash: await calculateSha256(filepath),
    fileType,
    layer: detectLayer(relativePath),
    purpose: `Represents the file artifact at ${relativePath}.`
  };
}

// -------------------------------------------------------------
// AST-verktyg
// -------------------------------------------------------------
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

// -------------------------------------------------------------
// Vue-komponentanalys
// -------------------------------------------------------------
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

  // <template>-del
  const templateAst = programAst?.templateBody;
  if (templateAst) {
    traverse(templateAst, {
      enter(node) {
        if (node.type === 'VElement') {
          const tagName = node.name;
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

// -------------------------------------------------------------
// Pinia store-analys
// -------------------------------------------------------------
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

// -------------------------------------------------------------
// Router-analys (robust)
// -------------------------------------------------------------
function analyzeRouter(ast, fileId, rootDir) {
  const nodes = [];
  const edges = [];
  const imports = new Map();

  // Samla alla top-level importer
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

  // Hitta och analysera routes-arrayen
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

            // statisk import (component: HomePage)
            if (key === 'component' && prop.value?.type === 'Identifier') {
              componentIdentifierName = prop.value.name;
            }
            // dynamisk import (component: () => import(...))
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

// -------------------------------------------------------------
// SAAP: laddning, standard, validering
// -------------------------------------------------------------
{
  "protocolId": "P-SAAP-1.2",
  "title": "System Architecture Adherence Protocol",
  "version": "1.2.0",
  "strict_mode": true,
  "fail_fast": false,

  "architecturalLayers": [
    { "layer": 0, "name": "shared",   "layerPathPattern": "src/shared/**/*" },
    { "layer": 1, "name": "entities", "layerPathPattern": "src/entities/**/*" },
    { "layer": 2, "name": "features", "layerPathPattern": "src/features/**/*" },
    { "layer": 3, "name": "widgets",  "layerPathPattern": "src/widgets/**/*" },
    { "layer": 4, "name": "pages",    "layerPathPattern": "src/pages/**/*" },
    { "layer": 5, "name": "app",      "layerPathPattern": "src/app/**/*" }
  ],

  "placementRules": [
    { "fileType": "VueComponent", "allowedPath": "src/App.vue" },
    { "fileType": "VueComponent", "allowedPath": "src/shared/ui/**/*.vue" },
    { "fileType": "VueComponent", "allowedPath": "src/features/**/ui/**/*.vue" },
    { "fileType": "VueComponent", "allowedPath": "src/widgets/**/*.vue" },       // täcker både widgets/*/*.vue och widgets/**/ui/*.vue
    { "fileType": "VueComponent", "allowedPath": "src/pages/**/*.vue" },
    { "fileType": "RouterConfig", "allowedPath": "src/app/router.js" }
  ],

  "dependencyRules": [
    { "from": "app",      "to": ["app","pages","widgets","features","entities","shared"] },
    { "from": "pages",    "to": ["pages","widgets","features","entities","shared"] },
    { "from": "widgets",  "to": ["widgets","features","entities","shared"] },
    { "from": "features", "to": ["features","entities","shared"] },
    { "from": "entities", "to": ["entities","shared"] },
    { "from": "shared",   "to": ["shared"] }
  ]
}

function ruleAllows(fromLayer, toLayer, saap) {
  const names = new Set((saap.architecturalLayers || []).map(l => l.name));
  if (toLayer === 'public' || toLayer === 'external' || toLayer === 'BinaryAsset' || toLayer === 'StaticData') return true;
  if (!names.has(fromLayer) || !names.has(toLayer)) return true;
  const r = (saap.dependencyRules || []).find(x => x.from === fromLayer);
  return !!(r && r.to.includes(toLayer));
}

function validatePlacementForNode(node, saap) {
  const rules = (saap.placementRules || []).filter(r => r.fileType === node.fileType);
  if (rules.length === 0) return null;
  const ok = rules.some(r => minimatch(node.path, r.allowedPath, { dot: true }));
  if (ok) return null;
  return {
    type: 'PLACEMENT',
    path: node.path,
    fileType: node.fileType,
    layer: node.layer,
    rules: rules.map(r => r.allowedPath)
  };
}

function normalizeTarget(target) {
  if (typeof target !== 'string') return String(target);
  if (target.startsWith('@/')) return target.replace('@/', 'src/');
  return target;
}

function isFilePathLike(p) {
  return typeof p === 'string' && (p.startsWith('src/') || p.startsWith('public/'));
}

function validateDependencyEdge(edge, saap) {
  const relevantTypes = new Set(['IMPORTS', 'USES_COMPONENT', 'USES_STORE_FILE', 'RENDERS_COMPONENT']);
  if (!relevantTypes.has(edge.type)) return null;
  const source = normalizeTarget(edge.source);
  const target = normalizeTarget(edge.target);

  if (!isFilePathLike(source) || !isFilePathLike(target)) return null;

  const fromLayer = detectLayer(source);
  const toLayer = detectLayer(target);
  const allowed = ruleAllows(fromLayer, toLayer, saap);
  if (allowed) return null;

  const rule = (saap.dependencyRules || []).find(r => r.from === fromLayer) || null;
  return {
    type: 'DEPENDENCY',
    source,
    target,
    fromLayer,
    toLayer,
    rule,
    hint: `Tillåtet från '${fromLayer}' -> ${(rule && Array.isArray(rule.to)) ? JSON.stringify(rule.to) : '[]'}`
  };
}

function summarizeViolations(violations) {
  const summary = { total: violations.length, placement: 0, dependency: 0 };
  for (const v of violations) {
    if (v.type === 'PLACEMENT') summary.placement++;
    if (v.type === 'DEPENDENCY') summary.dependency++;
  }
  return summary;
}

// -------------------------------------------------------------
// Huvudlogik
// -------------------------------------------------------------
async function main(rootDir, outputFile, protocolFile, modeArg) {
  console.log('Startar generering av System Semantic Map (SSM) v4.7...');

  const allNodes = [];
  const allEdges = [];

  const targetPatterns = ['src/**/*.{js,ts,vue,json,css}', 'public/data/**/*.{json,webp}'];
  const files = await glob(targetPatterns, { cwd: rootDir, nodir: true });

  console.log(`  - Hittade ${files.length} relevanta filer...`);

  // Last-run cache från tidigare SSM
  let previous = null;
  let previousHashes = new Map();
  let previousNodesByPath = new Map();
  let previousEdgesBySource = new Map();
  try {
    const prev = JSON.parse(await fs.readFile(path.join(rootDir, outputFile), 'utf-8'));
    previous = prev;
    if (Array.isArray(prev.nodes)) {
      for (const n of prev.nodes) {
        if (n.type === 'File' && n.hash) previousHashes.set(n.path, n.hash);
        if (n.path) {
          if (!previousNodesByPath.has(n.path)) previousNodesByPath.set(n.path, []);
          previousNodesByPath.get(n.path).push(n);
        }
      }
    }
    if (Array.isArray(prev.edges)) {
      for (const e of prev.edges) {
        if (!e.source) continue;
        if (!previousEdgesBySource.has(e.source)) previousEdgesBySource.set(e.source, []);
        previousEdgesBySource.get(e.source).push(e);
      }
    }
  } catch { /* ingen tidigare cache */ }

  // SAAP laddning
  const { saap, origin } = await loadSAAP(rootDir, outputFile, protocolFile);
  CURRENT_SAAP = saap;
  const CLI_MODE = (modeArg || '').toUpperCase(); // STRICT | REPORT | ''
  const STRICT = CLI_MODE ? (CLI_MODE === 'STRICT') : !!saap.strict_mode;
  const FAIL_FAST = !!saap.fail_fast;

  console.log(`  - SAAP: källa: ${origin}; strict_mode=${STRICT}; fail_fast=${FAIL_FAST}`);

  // För-index över filers SHA
  const fileNodeCache = new Map();

  for (const relativePath of files.map(f => f.replace(/\\/g, '/'))) {
    const filepath = path.join(rootDir, relativePath);
    const fileNode = await createFileNode(filepath, rootDir);
    allNodes.push(fileNode);
    fileNodeCache.set(relativePath, fileNode);

    // Hoppa icke-kodfiler
    if (isBinary(filepath) || filepath.endsWith('.json') || filepath.endsWith('.css')) continue;

    // Hash-cache: återanvänd noder/kanter om oförändrat
    if (previousHashes.get(relativePath) === fileNode.hash) {
      const prevNodes = (previousNodesByPath.get(relativePath) || []).filter(n => n.type !== 'File');
      const prevEdges = previousEdgesBySource.get(relativePath) || [];
      if (prevNodes.length) allNodes.push(...prevNodes);
      if (prevEdges.length) allEdges.push(...prevEdges);
      continue;
    }

    try {
      const content = await fs.readFile(filepath, 'utf-8');

      let parsed;
      try {
        parsed = parseForESLint(content, {
          filePath: filepath,
          parser: tsParser,
          sourceType: 'module',
          ecmaVersion: 'latest'
        });
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
              const resolvedTarget = path
                .relative(rootDir, path.resolve(path.dirname(filepath), sourcePath))
                .replace(/\\/g, '/');
              allEdges.push({ source: relativePath, target: resolvedTarget, type: 'IMPORTS' });
            } else if (sourcePath.startsWith('@/')) {
              const resolvedTarget = sourcePath.replace('@/', 'src/');
              allEdges.push({ source: relativePath, target: resolvedTarget, type: 'IMPORTS' });
            } else {
              allEdges.push({ source: relativePath, target: sourcePath, type: 'IMPORTS_PACKAGE' });
              if (!allNodes.some(n => n.id === sourcePath && n.type === 'NpmPackage')) {
                allNodes.push({
                  id: sourcePath,
                  type: 'NpmPackage',
                  name: sourcePath,
                  purpose: `Represents the external NPM dependency '${sourcePath}'.`
                });
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
      allEdges.push({
        source: relativePath,
        target: 'PARSING_ERROR',
        type: 'HAS_ERROR',
        details: e.message
      });
    }
  }

  // SAAP-validering: placering
  const violations = [];
  for (const node of allNodes) {
    if (node.type !== 'File') continue;
    const v = validatePlacementForNode(node, saap);
    if (v) {
      violations.push(v);
      console.error(`SAAP[PLACEMENT]: ${v.path} (${v.fileType}) tillåts ej. Tillåtna mönster: ${v.rules.join(', ')}`);
      if (STRICT && FAIL_FAST) {
        const ssmFail = {
          "$schema": "./system_semantic_map.schema.json",
          "version": "4.7.0",
          "createdAt": new Date().toISOString(),
          "nodes": allNodes,
          "edges": allEdges,
          "saapSnapshot": saap,
          "validation": { violations, summary: summarizeViolations(violations) }
        };
        const outputPath = path.join(rootDir, outputFile);
        await fs.mkdir(path.dirname(outputPath), { recursive: true });
        await fs.writeFile(outputPath, JSON.stringify(ssmFail, null, 2));
        console.error('Avbryter p.g.a. fail_fast.');
        process.exitCode = 2;
        return;
      }
    }
  }

  // SAAP-validering: beroenden
  for (const edge of allEdges) {
    const v = validateDependencyEdge(edge, saap);
    if (v) {
      violations.push(v);
      console.error(`SAAP[DEPENDENCY]: ${v.source} (${v.fromLayer}) -> ${v.target} (${v.toLayer}) är otillåtet. ${v.hint}`);
      if (STRICT && FAIL_FAST) {
        const ssmFail = {
          "$schema": "./system_semantic_map.schema.json",
          "version": "4.7.0",
          "createdAt": new Date().toISOString(),
          "nodes": allNodes,
          "edges": allEdges,
          "saapSnapshot": saap,
          "validation": { violations, summary: summarizeViolations(violations) }
        };
        const outputPath = path.join(rootDir, outputFile);
        await fs.mkdir(path.dirname(outputPath), { recursive: true });
        await fs.writeFile(outputPath, JSON.stringify(ssmFail, null, 2));
        console.error('Avbryter p.g.a. fail_fast.');
        process.exitCode = 2;
        return;
      }
    }
  }

  const summary = summarizeViolations(violations);

  const ssm = {
    "$schema": "./system_semantic_map.schema.json",
    "version": "4.7.0",
    "createdAt": new Date().toISOString(),
    "nodes": allNodes,
    "edges": allEdges,
    "protocolId": saap.protocolId,
    "title": saap.title,
    "strict_mode": STRICT,
    "fail_fast": FAIL_FAST,
    "architecturalLayers": saap.architecturalLayers,
    "placementRules": saap.placementRules,
    "dependencyRules": saap.dependencyRules,
    "saapSnapshot": saap,
    "validation": { violations, summary }
  };

  const outputPath = path.join(rootDir, outputFile);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(ssm, null, 2));

  console.log(`\nSSM v4.7 genererad.`);
  console.log(`  - Noder: ${allNodes.length}`);
  console.log(`  - Kanter: ${allEdges.length}`);
  console.log(`  - Regler: placement=${(saap.placementRules||[]).length}, dependency=${(saap.dependencyRules||[]).length}`);
  console.log(`  - SAAP-källa: ${origin}`);
  console.log(`  - Validering: total=${summary.total}, placement=${summary.placement}, dependency=${summary.dependency}`);
  console.log(`  - Output: ${outputFile}`);

  if (STRICT && summary.total > 0) {
    console.error('Strict mode aktivt och överträdelser finns. Avslutar med felkod 2.');
    process.exitCode = 2;
  }
}

// -------------------------------------------------------------
// CLI
// -------------------------------------------------------------
const argv = process.argv.slice(2);
function getFlag(name) {
  return argv.some(a => a.toLowerCase() === name.toLowerCase());
}
function firstNonFlag(startIdx = 0) {
  let count = 0;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('-')) continue;
    if (count === startIdx) return a;
    count++;
  }
  return undefined;
}

// Parametrar i ordning: rootDir, outputFile, protocolFile, mode
const rootDir = firstNonFlag(0) || '.';
const outputFile = firstNonFlag(1) || 'scripts/vuemap/system_semantic_map.json';
const protocolFile = firstNonFlag(2) || 'scripts/vuemap/saap.protocol.json';
const hasInit = getFlag('--init') || getFlag('--INIT');
const isStrict = getFlag('STRICT');
const isReport = getFlag('REPORT');
const modeArg = isStrict ? 'STRICT' : (isReport ? 'REPORT' : '');

// --INIT: materialisera SAAP och avsluta
if (hasInit) {
  const abs = path.join(rootDir, protocolFile);
  const exists = await fileExists(abs);
  if (!exists) {
    const base = defaultSAAP();
    await fs.mkdir(path.dirname(abs), { recursive: true });
    await fs.writeFile(abs, JSON.stringify(base, null, 2));
    console.log(`Skapade SAAP: ${protocolFile}`);
  } else {
    console.log(`SAAP finns redan: ${protocolFile}`);
  }
  process.exit(0);
}

// Kör
await main(rootDir, outputFile, protocolFile, modeArg).catch(err => {
  console.error(err);
  process.exitCode = 1;
});
