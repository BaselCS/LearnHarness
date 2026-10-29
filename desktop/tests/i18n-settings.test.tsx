/**
 * The settings surface in Spanish and Arabic: the sections render the provider's
 * language (copy, aria labels, placeholders) while testids stay English,
 * and render English when no provider is mounted.
 */
import React from "react";
(globalThis as Record<string, unknown>).React = React;

import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { renderToStaticMarkup } from "react-dom/server";
import { I18nProvider } from "../components/i18n.tsx";
import { GeneralSection } from "../components/settings/settings-dialog.tsx";
import { KeysSection, keyStatusLine } from "../components/settings/keys-section.tsx";

const es = (node: React.ReactNode) => renderToStaticMarkup(<I18nProvider initialLanguage="es">{node}</I18nProvider>);
const ar = (node: React.ReactNode) => renderToStaticMarkup(<I18nProvider initialLanguage="ar">{node}</I18nProvider>);

describe("settings sections under the Spanish provider", () => {
	it("GeneralSection: the dictation override rows read Spanish", () => {
		const html = es(<GeneralSection general={{ language: "es" }} onChange={() => {}} />);
		assert.ok(html.includes("Usar otro idioma para el dictado"));
		assert.ok(html.includes("Idioma del dictado"));
		assert.ok(html.includes("Multilingüe (detección automática)"));
	});

	it("KeysSection: the SSR loading state reads Spanish", () => {
		assert.ok(es(<KeysSection />).includes("Cargando claves…"));
	});

	it("pure helpers take the language, English by default", () => {
		const unset = { id: "X", info: null, present: false, masked: null, source: "none", shadowedByEnv: false } as const;
		assert.equal(keyStatusLine(unset, "es"), "sin configurar");
		assert.equal(keyStatusLine(unset), "not set");
		assert.equal(keyStatusLine(unset, "ar"), "غير مضبوط");
	});
});

describe("settings sections under the Arabic provider", () => {
	it("GeneralSection: the dictation override rows read Arabic", () => {
		const html = ar(<GeneralSection general={{ language: "ar" }} onChange={() => {}} />);
		assert.ok(html.includes("استخدام لغة أخرى للإملاء الصوتي"));
		assert.ok(html.includes("لغة الإملاء الصوتي"));
		assert.ok(html.includes("متعدد اللغات (اكتشاف تلقائي)"));
	});

	it("KeysSection: the SSR loading state reads Arabic", () => {
		assert.ok(ar(<KeysSection />).includes("جارٍ تحميل المفاتيح…"));
	});
});

describe("settings sections without a provider", () => {
	it("render English", () => {
		const html = renderToStaticMarkup(<KeysSection />);
		assert.ok(html.includes("Loading keys…"));
	});
});
