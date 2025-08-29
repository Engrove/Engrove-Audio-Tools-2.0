// scripts/vuemap/generate-ssm.mjs
// v2.0
// === SYFTE & ANSVAR ===
// Detta Node.js-skript genererar en System Semantic Map (SSM) i JSON-format.
// Det använder industristandardverktyg (@vue/compiler-sfc, vue-eslint-parser)
// för att tillförlitligt parsa modern Vue 3 och JavaScript-syntax (ES2020+).
// === HISTORIK ===
// v1.x: (Avvecklad) Python-version som misslyckades p.g.a. inkompatibel parser.
// v2.0: (Help me God - Domslut) Omskriven till Node.js för att använda det
//       nativa verktygsekosystemet, vilket löser alla tidigare parseringsfel.

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';
import { parse as parseSfc } from '@vue/compiler-sfc';
import { parseForESLint } from 'vue-eslint-parser';

// --- Kärnfunktioner ---

async function calculateSha256(filepath) {
  const fileBuffer = await fs.readFile(filepath);
  return crypto.createHash('sha256').update(fileBuffer).digest('hex');
}

function isBinary(filepath) {
  const binaryExtensions = ['.webp', '.jpg', '.jpeg', '.gif', '.png', '.pdf'];
  return binaryExtensions.some(ext => filepath.toLowerCase().endsWith(ext));
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
            continue; // Bearbeta inte innehållet för dessa filer just nu
        }

        try {
            const content = await fs.readFile(filepath, 'utf-8');
            const ast = parseForESLint(content, {
                parser: '@typescript-eslint/parser', // En robust parser
                sourceType: 'module',
                ecmaVersion: 'latest'
            }).ast;
            
            // Extrahera importer
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
        "version": "2.0.0",
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

// Kör skriptet
const rootDir = process.argv[2] || '.';
const outputFile = process.argv[3] || 'scripts/vuemap/system_semantic_map.json';
main(rootDir, outputFile).catch(console.error);
