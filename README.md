This library reproduces the scoring scheme from
[riveter-nlp](https://github.com/maartensap/riveter-nlp). Basically,
this is the part of `riveter-nlp` that only assigns scores to data
given a lexicon. 

We composed `riveter-scorer` for convinience of another project that
relies on the research that went into `riveter-nlp` but has different
needs.

## Install

```{shell}
uv add https://github.com/paskn/riveter-scorer.git
```

## Development

To run tests:

```{shell}
uv run python -Im pytest
```
