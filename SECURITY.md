# Security policy

This project is an academic prototype. Do not expose it to unrestricted public traffic or upload confidential PDFs.

## Reporting

If you find a vulnerability, use GitHub private vulnerability reporting if enabled, or contact the repository owner privately. Do not include credentials or sensitive document contents in public issues.

## Credential handling

Keep Pinecone and OpenRouter keys in local environment variables or a protected runtime secret store. Never commit .env, private keys, uploaded PDFs or credential-bearing container images. Rotate any credential that has been exposed.

## Known limitations

Authentication, per-user authorization, upload size limits, rate limiting and document retention/deletion are not implemented. External model requests include retrieved document excerpts. HTTPS protects traffic in transit but is not access control. Restrict access until these limitations are addressed.
