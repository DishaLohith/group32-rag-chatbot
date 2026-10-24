# Baseline — raw response from the no-retrieval LLM

To get a baseline for our comparison, we asked Claude 14 GST questions in a new chat with no documents attached. This was our no-retrieval condition. We scored its answers by hand against our answer key.

- Tool: Claude (new conversation on claude.ai)
- Run by: Tejas Gangadhar Gowda (s4235124)
- Date run: Not recorded
- Web search: Not recorded
- Note: the reply mentions our RAG project, so the chat may have had memory of earlier conversations

## Prompt (as sent)

1. Is plain bread rolls sold in a supermarket GST-free or taxable under Australian GST law?
2. Is bread rolls served in a restaurant GST-free or taxable?
3. Is plain milk GST-free or taxable?
4. Is flavoured chocolate milk GST-free or taxable?
5. Is raw chicken GST-free or taxable?
6. Is hot roast chicken ready to eat GST-free or taxable?
7. Is chocolate/confectionery GST-free or taxable?
8. Is carbonated soft drink GST-free or taxable?
9. Is fruit juice with 90%+ juice content GST-free or taxable?
10. Is plain unsalted raw almonds GST-free or taxable?
11. Is roasted salted almonds GST-free or taxable?
12. Is still bottled unflavoured water GST-free or taxable?
13. Is sparkling mineral water GST-free or taxable?
14. Are rice cakes GST-free or taxable?

## Response (verbatim)

These all turn on the same Australian GST basic food rules (GST Act, Schedule 1 to A New Tax System (Goods and Services Tax) Act 1999). Here's each one:

1. Plain bread rolls (supermarket) — GST-free. Basic bread and bread rolls without a sweet coating or filling are GST-free.
2. Bread rolls served in a restaurant — Taxable. Food supplied "for consumption on the premises" (restaurant, café dine-in) is always taxable, regardless of what the food itself is.
3. Plain milk — GST-free. Milk is a listed GST-free beverage.
4. Flavoured chocolate milk — Taxable. Flavoured milk (e.g., chocolate, strawberry) is specifically excluded from the milk exemption and taxed as a flavoured beverage.
5. Raw chicken — GST-free. Uncooked meat for human consumption is GST-free.
6. Hot roast chicken, ready to eat — Taxable. Food sold hot for consumption ("hot food") is taxable — this is the specific carve-out that catches hot roast chickens, hot chips, etc.
7. Chocolate/confectionery — Taxable. Confectionery is specifically excluded from GST-free food.
8. Carbonated soft drink — Taxable. Carbonated/flavoured drinks are taxable beverages.
9. Fruit juice, 90%+ juice content — GST-free. Juice of fruit/vegetables is GST-free only if it contains at least 90% by volume of juice; below that threshold it's taxable.
10. Plain unsalted raw almonds — GST-free. Unprocessed/unflavoured nuts are GST-free (food for human consumption that isn't otherwise excluded).
11. Roasted salted almonds — Taxable. Once nuts are flavoured/processed (salted, roasted with seasoning), they fall under the "savoury snack food" exclusion and become taxable.
12. Still bottled unflavoured water — Taxable. Plain bottled drinking water is specifically excluded from GST-free status (it's a taxable beverage), even though tap water itself is GST-free.
13. Sparkling mineral water — Taxable. Also excluded as a beverage, same as still bottled water.
14. Rice cakes — Depends on type, but plain rice cakes marketed as a substitute for bread/crackers are generally GST-free; if they're flavoured/coated or marketed as a snack food/confectionery, they become taxable. Worth checking the specific product against ATO's food classification guidance if this matters for your assignment — this one's a genuine edge case in practice, and the ATO's detailed food list is the authority to cite.

If this is for your RAG GST chatbot project, the ATO's detailed food list (GST food guide) is the primary source you'd want the model grounded in, since a lot of these edge cases (like rice cakes) hinge on marketing/packaging specifics rather than a clean rule.

## How we scored it

We checked the answers against our answer key by hand. For the main comparison, we used items 1–13 and reported GST14 separately, because its expected answer was changed from Abstain to GST-free after the baseline was run.

On items 1–13, the baseline got 12 correct out of 13 (92.3%). Its macro-F1 was 0.921, and its attribution score was 0% because it did not cite any specific supporting passages. The results are in `baseline_results.md`.
