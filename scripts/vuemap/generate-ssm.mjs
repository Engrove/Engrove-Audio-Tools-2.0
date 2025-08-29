// scripts/vuemap/generate-ssm.mjs
// v3.1
// === SYFTE & ANSVAR ===
// Detta Node.js-skript genererar en System Semantic Map (SSM) i JSON-format.
// Det använder industristandardverktyg för att tillförlitligt parsa modern
// Vue 3 och JavaScript-syntax (ES2020+).
// === HISTORIK ===
// v3.0: Uppgraderad för att parsa Pinia stores och interna relationer.
// v3.1: (Help me God - Domslut) Korrigerat ett kritiskt importfel. Byt ut
//       den felaktiga 'traverse' från 'eslint-visitor-keys' mot den korrekta
//       'traverseNodes' från 'vue-eslint-parser' för att lösa SyntaxError.

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';
import { parseForESLint, traverseNodes } from 'vue-eslint-parser'; // KORRIGERAD IMPORT

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
    if (filepath.endsWith('.js')) {
        if (filepath.toLowerCase().includes('store')) return 'PiniaStore';
        if (filepath.toLowerCase().includes('router')) return 'Configuration';
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
        fileType: fileType,
        purpose: `Represents the file artifact at ${relativePath}.`
    };
}

// --- AST Analys & Berikning ---

function analyzePiniaStore(ast, fileId) {
    const storeNodes = [];
    const storeEdges = [];
    let storeId = null;
    let mainStoreNode = null;

    traverseNodes(ast, { // KORRIGERAT FUNKTIONSANROP
        enter(node) {
            if (node.type === 'CallExpression' && node.callee.name === 'defineStore') {
                if (node.arguments.length > 0 && node.arguments[0].type === 'Literal') {
                    storeId = node.arguments[0].value;
                }
                
                mainStoreNode = {
                    id: storeId,
                    type: 'Store',
                    path: fileId,
                    storeId: storeId,
                    purpose: `Manages state for the '${storeId}' domain.`
                };
                storeNodes.push(mainStoreNode);
                storeEdges.push({ source: fileId, target: storeId, type: 'DEFINES' });

                const storeDefinition = node.arguments[1];
                if (storeDefinition && storeDefinition.type === 'ObjectExpression') {
                    // --- STATE ---
                    const stateProp = storeDefinition.properties.find(p => p.key.name === 'state');
                    if (stateProp && stateProp.value.type === 'ArrowFunctionExpression' && stateProp.value.body.type === 'ObjectExpression') {
                        stateProp.value.body.properties.forEach(prop => {
                            const stateNode = {
                                id: `${storeId}#state.${prop.key.name}`,
                                type: 'StateVariable',
                                path: fileId,
                                parent: storeId,
                                dataType: 'Unknown',
                                purpose: `Represents the '${prop.key.name}' state property.`
                            };
                            storeNodes.push(stateNode);
                            storeEdges.push({ source: storeId, target: stateNode.id, type: 'DEFINES' });
                        });
                    }

                    // --- GETTERS & ACTIONS ---
                    ['getters', 'actions'].forEach(section => {
                        const propSection = storeDefinition.properties.find(p => p.key.name === section);
                        if (propSection && propSection.value.type === 'ObjectExpression') {
                            propSection.value.properties.forEach(prop => {
                                const propType = section === 'getters' ? 'Getter' : 'Action';
                                const propNode = {
                                    id: `${storeId}#${section}.${prop.key.name}`,
                                    type: propType,
                                    path: fileId,
                                    parent: storeId,
                                    purpose: `A ${section.slice(0, -1)} for the '${storeId}' store.`
                                };
                                storeNodes.push(propNode);
                                storeEdges.push({ source: storeId, target: propNode.id, type: 'DEFINES' });

                                traverseNodes(prop.value.body, { // KORRIGERAT FUNKTIONSANROP
                                    enter(childNode, parentNode) {
                                        if (childNode.type === 'MemberExpression' && childNode.object.type === 'ThisExpression') {
                                            const propertyName = childNode.property.name;
                                            const stateId = `${storeId}#state.${propertyName}`;
                                            
                                            if (parentNode.type === 'AssignmentExpression' && parentNode.left === childNode) {
                                                storeEdges.push({ source: propNode.id, target: stateId, type: 'MODIFIES_STATE' });
                                            } else {
                                                storeEdges.push({ source: propNode.id, target: stateId, type: 'READS_STATE' });
                                            }
                                        }
                                        if(childNode.type === 'CallExpression' && childNode.callee.type === 'MemberExpression' && childNode.callee.object.type === 'ThisExpression') {
                                            const calleeName = childNode.callee.property.name;
                                            const targetId = `${storeId}#actions.${calleeName}`;
                                            storeEdges.push({ source: propNode.id, target: targetId, type: 'CALLS' });
                                        }
                                    }
                                });
                            });
                        }
                    });
                }
            }
        }
    });

    return { nodes: storeNodes, edges: storeEdges };
}


// --- Huvudlogik ---

async function main(rootDir, outputFile) {
    console.log("Startar generering av System Semantic Map (SSM)...");
    
    const allNodes = [];
    const allEdges = [];
    
    const targetPatterns = ['src/**/*.{js,vue,json,css}', 'public/data/**/*.{json,webp}'];
    const files = await glob(targetPatterns, { cwd: rootDir, nodir: true });

    console.log(`  - Hittade ${files.length} relevanta filer...`);

    for (const relativePath of files) {
        const filepath = path.join(rootDir, relativePath);

        const fileNode = await createFileNode(filepath, rootDir);
        allNodes.push(fileNode);

        if (isBinary(filepath) || filepath.endsWith('.json') || filepath.endsWith('.css')) {
            continue;
        }

        try {
            const content = await fs.readFile(filepath, 'utf-8');
            const ast = parseForESLint(content, {
                parser: '@typescript-eslint/parser',
                sourceType: 'module',
                ecmaVersion: 'latest'
            }).ast;
            
            if (ast.body) {
                for (const node of ast.body) {
                    if (node.type === 'ImportDeclaration' && node.source && node.source.value) {
                        allEdges.push({
                            source: relativePath,
                            target: node.source.value,
                            type: 'IMPORTS'
                        });
                    }
                }
            }

            if (fileNode.fileType === 'PiniaStore') {
                const { nodes: storeNodes, edges: storeEdges } = analyzePiniaStore(ast, relativePath);
                allNodes.push(...storeNodes);
                allEdges.push(...storeEdges);
            }

        } catch (e) {
            console.warn(`    - Varning: Kunde inte parsa ${relativePath}: ${e.message}`);
             allEdges.push({
                source: relativePath,
                target: "PARSING_ERROR",
                type: "HAS_ERROR",
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
main(rootDir, outputFile).catch(console.error);
