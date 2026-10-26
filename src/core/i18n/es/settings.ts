import type { settings as en } from "../en/settings.ts";

export const settings: Record<keyof typeof en, string> = {
	"settings.title": "Ajustes",
	"settings.close": "Cerrar ajustes",
	"settings.nav": "Secciones de ajustes",
	"settings.loading": "Cargando ajustes…",
	"settings.loadFailed": "No se pudieron cargar los ajustes — recarga para reintentar.",
	"settings.section.keys": "Proveedores",
	"settings.section.agent": "Agente",
	"settings.section.appearance": "Apariencia",
	"settings.section.graph": "Grafo",
	"settings.section.keyboard": "Teclado",
	"settings.section.keyboard.hint": "Se guarda en este dispositivo",
	"settings.section.general": "General",
	"settings.general.autoUpdate": "Actualización automática",
	"settings.general.autoUpdate.aria": "actualización automática",
	"settings.general.autoUpdate.hint": "Las actualizaciones automáticas llegarán en una próxima versión",
	"settings.general.language": "Idioma",
	"settings.general.language.aria": "idioma",
};
