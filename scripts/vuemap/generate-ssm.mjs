// scripts/vuemap/generate-ssm.mjs
// v3.6
// === SYFTE & ANSVAR ===
// Detta Node.js-skript genererar en System Semantic Map (SSM) i JSON-format.
// Det använder industristandardverktyg för att tillförlitligt parsa modern
// Vue 3- och JavaScript-syntax (ES2020+).
// === HISTORIK ===
// v3.0: Uppgraderad för att parsa Pinia stores och interna relationer.
// v3.1: (Help me God - Domslut) Korrigerat kritiskt importfel; bort med felaktig 'traverse'.
// v3.2: Korrigerad ESM/CJS-interoperabilitet för 'vue-eslint-parser'.
// v3.5: Slutlig interop-fix för default-import.
// v3.6: Egen generisk AST-traverser utan externa beroenden. Robust hantering av getters/actions.

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
  if (filepath.endsWith('.vue')) return 'VueComponent';
  if (filepath.endsWith('.js') || filepath.endsWith('.mjs') || filepath.endsWith('.ts')) {
    const lower = filepath.toLowerCase();
    if (lower.includes('store')) return 'PiniaStore';
    if (lower.includes('router')) return 'Configuration';
    return 'Utility';
  }
  if (filepath.endsWith('.json')) return 'StaticData';
  if (isBinary(filepath)) return 'BinaryAsset';
  return 'Other';
}

async function createFileNode(filepath, rootDir) {
  const relativePath = path.relative(rootDir, filepath);
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
function safePropName(prop) {
  if (!prop) return undefined;
  // Support Identifier, Literal, PrivateIdentifier rare
  if (prop.key?.name) return prop.key.name;
  if (prop.key?.value) return String(prop.key.value);
  return undefined;
}

function analyzePiniaStore(ast, fileId) {
  const storeNodes = [];
  const storeEdges = [];

  traverse(ast, {
    enter(node) {
      if (node.type === 'CallExpression' && node.callee?.name === 'defineStore') {
        // store id
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

          // STATE
          const stateProp = props.find(p => safePropName(p) === 'state');
          // state: () => ({ ... })
          let stateObj = null;
          if (stateProp?.value?.type === 'ArrowFunctionExpression' || stateProp?.value?.type === 'FunctionExpression') {
            const body = stateProp.value.body;
            // handle "return { ... }" in FunctionExpression body
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

          // GETTERS + ACTIONS
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

                // normalize body node for traversal: either BlockStatement or Expression
                const bodyNode = body;

                traverse(bodyNode, {
                  enter(childNode, parentNode) {
                    // this.<prop> usage
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
                    // this.action() calls
                    if (childNode.type === 'CallExpression'
                      && childNode.callee?.type === 'MemberExpression'
                      && childNode.callee.object?.type === 'ThisExpression') {
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

// --- Huvudlogik ---
async function main(rootDir, outputFile) {
  console.log('Startar generering av System Semantic Map (SSM)...');

  const allNodes = [];
  const allEdges = [];

  const targetPatterns = ['src/**/*.{js,ts,vue,json,css}', 'public/data/**/*.{json,webp}'];
  const files = await glob(targetPatterns, { cwd: rootDir, nodir: true });

  console.log(`  - Hittade ${files.length} relevanta filer...`);

  for (const relativePath of files) {
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
      });
      const ast = parsed.ast;

      // Import edges
      if (ast?.body) {
        for (const node of ast.body) {
          if (node.type === 'ImportDeclaration' && node.source?.value) {
            allEdges.push({ source: relativePath, target: node.source.value, type: 'IMPORTS' });
          }
        }
      }

      // Pinia store analysis
      if (fileNode.fileType === 'PiniaStore') {
        const { nodes: storeNodes, edges: storeEdges } = analyzePiniaStore(ast, relativePath);
        allNodes.push(...storeNodes);
        allEdges.push(...storeEdges);
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
    "version": "3.1.0",
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
