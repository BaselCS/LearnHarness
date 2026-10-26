/**
 * THE APP LANGUAGE REGISTRY — the one list of languages the app speaks.
 * Adding a language: one entry here, one UI dictionary (i18n/<id>.ts,
 * typed as Dictionary so missing keys fail typecheck), one mirrored tree
 * of translated prompt segments (src/agent/prompts/locales/<id>/) and an
 * <id> entry in each inline worker prompt map. Anything not yet translated
 * falls back to English, the source of truth.
 *
 * Browser-safe: pure data + logic, no node imports.
 */

export const APP_LANGUAGES = [
	{ id: "en", label: "English", dictation: "en" },
	{ id: "es", label: "Español", dictation: "es" },
] as const;

export type AppLanguage = (typeof APP_LANGUAGES)[number]["id"];

export const DEFAULT_LANGUAGE: AppLanguage = "en";

export function isAppLanguage(value: unknown): value is AppLanguage {
	return APP_LANGUAGES.some((lang) => lang.id === value);
}

/** Per-language variants of one text; English is required, the rest fall back to it. */
export type Localized<T> = { en: T } & Partial<Record<AppLanguage, T>>;

export function pickLocalized<T>(map: Localized<T>, language: AppLanguage = DEFAULT_LANGUAGE): T {
	return map[language] ?? map.en;
}

/** The Deepgram `language` code dictation uses for an app language. */
export function dictationCodeFor(language: AppLanguage): string {
	return APP_LANGUAGES.find((lang) => lang.id === language)?.dictation ?? "en";
}
