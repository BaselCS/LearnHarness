import fs from "node:fs";
import path from "node:path";

const ANKI_CONNECT_URL = "http://127.0.0.1:8765";
const DEFAULT_DECK = "LearnHarness::AI";
const PENDING_FILE = path.join(process.cwd(), "pending_cards.json");

export interface AnkiCardPayload {
	id: string;
	deckName?: string;
	modelName?: "Cloze" | "Basic";
	fields: {
		Front?: string;
		Back?: string;
		Text?: string;
		Extra?: string;
	};
	tags?: string[];
}

export class AnkiService {
	static async ping(): Promise<boolean> {
		try {
			const res = await fetch(ANKI_CONNECT_URL, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ action: "version", version: 6 }),
			});
			if (!res.ok) return false;
			const data = (await res.json()) as { error?: string | null };
			return !data.error;
		} catch {
			return false;
		}
	}

	static async ensureDeckAndModel(deckName = DEFAULT_DECK): Promise<void> {
		try {
			await fetch(ANKI_CONNECT_URL, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					action: "createDeck",
					version: 6,
					params: { deck: deckName },
				}),
			});
		} catch {
			// ignore if offline
		}
	}

	static async addCard(
		card: AnkiCardPayload
	): Promise<{ success: boolean; noteId?: number; queued?: boolean }> {
		const isUp = await this.ping();
		const deck = card.deckName || DEFAULT_DECK;
		const model = card.modelName || (card.fields.Text ? "Cloze" : "Basic");
		const tags = Array.from(new Set([...(card.tags || []), "learnharness", `concept::${card.id}`]));

		if (!isUp) {
			this.queueCard(card);
			return { success: true, queued: true };
		}

		await this.ensureDeckAndModel(deck);

		try {
			const res = await fetch(ANKI_CONNECT_URL, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					action: "addNote",
					version: 6,
					params: {
						note: {
							deckName: deck,
							modelName: model,
							fields: card.fields,
							tags,
							options: {
								allowDuplicate: false,
								duplicateScope: "deck",
							},
						},
					},
				}),
			});
			const data = (await res.json()) as { result?: number; error?: string | null };
			if (data.error) {
				this.queueCard(card);
				return { success: false, queued: true };
			}
			// Attempt to drain queue if available
			this.syncPendingQueue().catch(() => {});
			return { success: true, noteId: data.result };
		} catch {
			this.queueCard(card);
			return { success: true, queued: true };
		}
	}

	private static queueCard(card: AnkiCardPayload): void {
		try {
			let queue: AnkiCardPayload[] = [];
			if (fs.existsSync(PENDING_FILE)) {
				queue = JSON.parse(fs.readFileSync(PENDING_FILE, "utf-8")) as AnkiCardPayload[];
			}
			queue.push(card);
			fs.writeFileSync(PENDING_FILE, JSON.stringify(queue, null, 2), "utf-8");
		} catch (err) {
			console.error("Failed to queue card:", err);
		}
	}

	static async syncPendingQueue(): Promise<{ synced: number; remaining: number }> {
		if (!fs.existsSync(PENDING_FILE)) return { synced: 0, remaining: 0 };
		const isUp = await this.ping();
		if (!isUp) return { synced: 0, remaining: 0 };

		let queue: AnkiCardPayload[] = [];
		try {
			queue = JSON.parse(fs.readFileSync(PENDING_FILE, "utf-8")) as AnkiCardPayload[];
		} catch {
			return { synced: 0, remaining: 0 };
		}

		const remaining: AnkiCardPayload[] = [];
		let synced = 0;

		for (const card of queue) {
			const deck = card.deckName || DEFAULT_DECK;
			const model = card.modelName || (card.fields.Text ? "Cloze" : "Basic");
			const tags = Array.from(new Set([...(card.tags || []), "learnharness", `concept::${card.id}`]));

			try {
				const res = await fetch(ANKI_CONNECT_URL, {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						action: "addNote",
						version: 6,
						params: {
							note: {
								deckName: deck,
								modelName: model,
								fields: card.fields,
								tags,
								options: {
									allowDuplicate: false,
									duplicateScope: "deck",
								},
							},
						},
					}),
				});
				const data = (await res.json()) as { error?: string | null };
				if (!data.error) {
					synced++;
				} else {
					remaining.push(card);
				}
			} catch {
				remaining.push(card);
			}
		}

		if (remaining.length === 0) {
			try {
				fs.unlinkSync(PENDING_FILE);
			} catch {}
		} else {
			fs.writeFileSync(PENDING_FILE, JSON.stringify(remaining, null, 2), "utf-8");
		}

		return { synced, remaining: remaining.length };
	}
}
