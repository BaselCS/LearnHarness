import fs from "node:fs";
import path from "node:path";

const DATA_GRAPH_DIR = path.resolve(process.cwd(), "data", "graph");
const NODES_FILE = path.join(DATA_GRAPH_DIR, "nodes.jsonl");
const CHAINS_FILE = path.join(DATA_GRAPH_DIR, "chains.jsonl");

export interface AGYConceptInput {
	name: string;
	statement: string;
	premises?: string[]; // IDs of prerequisites
}

export function injectConceptToGUI(concept: AGYConceptInput): { id: string; chainId?: string } {
	fs.mkdirSync(DATA_GRAPH_DIR, { recursive: true });

	const now = new Date().toISOString();
	const nodeId = `n_${Math.random().toString(36).substring(2, 10)}`;

	const nodeRecord = {
		id: nodeId,
		name: concept.name,
		statement: concept.statement,
		aliases: [concept.name],
		createdAt: now,
		provenance: [
			{
				chatId: "agy_session",
				messageId: "m_agy",
				at: now,
			},
		],
	};

	fs.appendFileSync(NODES_FILE, `${JSON.stringify(nodeRecord)}\n`, "utf-8");

	let chainId: string | undefined;
	if (concept.premises && concept.premises.length > 0) {
		chainId = `arg_${Math.random().toString(36).substring(2, 10)}`;
		const chainRecord = {
			id: chainId,
			premises: concept.premises,
			conclusion: nodeId,
			provenance: [
				{
					chatId: "agy_session",
					messageId: "m_agy",
					at: now,
				},
			],
			createdAt: now,
		};
		fs.appendFileSync(CHAINS_FILE, `${JSON.stringify(chainRecord)}\n`, "utf-8");
	}

	return { id: nodeId, chainId };
}

if (process.argv[2] === "--test") {
	const v1 = injectConceptToGUI({
		name: "Vector as Spatial Arrow",
		statement: "A vector in R^n represents a directed movement with magnitude and direction from the origin.",
	});
	const v2 = injectConceptToGUI({
		name: "Linear Transformation",
		statement: "A transformation T(v) is linear if T(cv+w) = cT(v)+T(w), mapping grid lines to parallel grid lines.",
		premises: [v1.id],
	});
	console.log("Injected concepts to LearnHarness GUI graph ledgers:", { v1, v2 });
}
