# API reference

The local base URL is http://127.0.0.1:8000. FastAPI exposes interactive documentation at /docs.

## Upload a PDF

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F 'file=@sample.pdf'
```

Example response (illustrative):

```json
{"doc_id":"example-document-id","filename":"sample.pdf","chunks":16}
```

The server assigns the document ID. Keep the actual returned ID for subsequent questions. Upload performs extraction, embedding and vector indexing synchronously.

## Ask a question

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is the main idea?","doc_id":"REPLACE_WITH_RETURNED_ID"}'
```

Example response:

```json
{"answer":"An answer based on retrieved passages."}
```

## Errors and limitations

- Non-PDF filenames and blank questions are rejected with HTTP 400.
- Invalid request schemas may return HTTP 422.
- Unhandled provider failures may return HTTP 500.
- Empty answers are retried up to three times; if exhausted, the endpoint returns an unavailability message rather than a generated answer.
- The document ID is a namespace selector, not an authentication credential.
- No server-side delete or user ownership endpoint is implemented.

Use only sample PDFs on a local or access-restricted deployment.
