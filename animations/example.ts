// Running example used by all LLM basics slides (token → … → next token).
// Token IDs are real o200k_base IDs (GPT-4o tokenizer), reproducible with:
//   uv run --with tiktoken python -c "import tiktoken; e = tiktoken.get_encoding('o200k_base'); \
//     print([(e.decode([i]), i) for i in e.encode('Aus dem kleinen Setzling wurde ein großer')])"
export const EXAMPLE_TOKENIZER = "o200k_base";
export const EXAMPLE_PROMPT = "Aus dem kleinen Setzling wurde ein großer";
export const EXAMPLE_TOKENS: [text: string, id: number][] = [
  ["Aus", 57115],
  [" dem", 2019],
  [" kleinen", 42535],
  [" Set", 3957],
  ["z", 89],
  ["ling", 3321],
  [" wurde", 11653],
  [" ein", 1605],
  [" großer", 86085],
];
export const EXAMPLE_ANSWER = " Baum";

// Next-token candidates (each a single o200k_base token) with illustrative logits.
// The values are made up for teaching; probabilities are derived via softmax so
// that temperature can be shown consistently.
export const EXAMPLE_CANDIDATES: [text: string, id: number, logit: number][] = [
  [" Baum", 70581, 6.1],
  [" Busch", 151135, 4.6],
  [" Wald", 57653, 4.1],
  [" Mann", 23959, 3.8],
  [" Erfolg", 62279, 3.0],
];

export function softmax(logits: number[], temperature = 1): number[] {
  const scaled = logits.map((logit) => logit / temperature);
  const max = Math.max(...scaled);
  const weights = scaled.map((value) => Math.exp(value - max));
  const sum = weights.reduce((a, b) => a + b, 0);
  return weights.map((weight) => weight / sum);
}

// Tokens are shown with a visible leading space.
export const visibleSpace = (text: string) => text.replace(/ /g, "␣");
