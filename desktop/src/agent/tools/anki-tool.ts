import { Type } from "typebox";
import type { AgentTool } from "@earendil-works/pi-agent-core";
import { serverExecute } from "../tool-execute.ts";
import { AnkiService } from "../../services/anki.ts";

const ankiCardInput = Type.Object({
	conceptId: Type.String({
		description: "Unique slug identifier for the concept, e.g. 'linalg_eigenvalues'",
	}),
	cardType: Type.Union([Type.Literal("Cloze"), Type.Literal("Basic")], {
		description: "Cloze deletion format or Basic Q&A format.",
	}),
	frontOrText: Type.String({
		description:
			"If Cloze: text containing {{c1::cloze deletion}} with concise math. If Basic: short question under 15 words.",
	}),
	backOrExtra: Type.Optional(
		Type.String({
			description:
				"If Basic: short 1-line answer or equation. If Cloze: optional extra context or derivation note.",
		}),
	),
	tags: Type.Optional(
		Type.Array(Type.String(), {
			description: "Tags for Anki, e.g. ['linear-algebra', 'eigenvalues']",
		}),
	),
});

export const syncAnkiCardTool: AgentTool<typeof ankiCardInput> = {
	name: "sync_anki_card",
	label: "sync_anki_card",
	description:
		"Automatically synthesizes and injects an atomic Anki flashcard (Cloze or Q&A) for a concept that has been thoroughly understood and mastered. Enforces the Minimum Information Principle.",
	parameters: ankiCardInput,
	execute: serverExecute(
		"sync_anki_card",
		ankiCardInput,
		async ({ conceptId, cardType, frontOrText, backOrExtra, tags }): Promise<string> => {
			const fields: Record<string, string> = {};
			if (cardType === "Cloze") {
				fields.Text = frontOrText;
				if (backOrExtra) fields.Extra = backOrExtra;
			} else {
				fields.Front = frontOrText;
				fields.Back = backOrExtra || "";
			}

			const result = await AnkiService.addCard({
				id: conceptId,
				modelName: cardType,
				fields,
				tags,
			});

			return result.queued
				? `Card for concept '${conceptId}' queued locally (Anki offline). Will sync automatically.`
				: `Card for concept '${conceptId}' successfully injected into Anki (Note ID: ${result.noteId}).`;
		},
	),
};
