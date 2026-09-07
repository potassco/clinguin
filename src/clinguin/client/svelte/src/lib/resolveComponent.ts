import type { Component } from "svelte";

type ComponentModule = Record<string, Component>;

const modules = import.meta.glob<ComponentModule>(
  "./components/ui/*/index.ts",
  { eager: true }
);

function toPascalCase(value: string): string {
  return value
    .split(/[_-]/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join("");
}

const namespaces: Record<string, ComponentModule> = {};

for (const [path, module] of Object.entries(modules)) {
  const folder = path.split("/").at(-2);
  if (folder) namespaces[toPascalCase(folder)] = module;
}

/** Resolves a component type string to a Svelte component. Returns null if not found. */
export function resolveComponent(type: string): Component | null {
  const match = type.match(/^(\w+)(?:\((\w+)\))?$/);
  if (!match) return null;

  const [, namespaceName, memberName] = match;
  const namespace = namespaces[toPascalCase(namespaceName)];

  if (!namespace) return null;

  if (memberName) {
    return namespace[toPascalCase(memberName)] ?? null;
  }

  return namespace.Root ?? namespace[toPascalCase(namespaceName)] ?? null;
}
