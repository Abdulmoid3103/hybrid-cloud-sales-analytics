# AWS deployment guide — future reference only

**Do not deploy these steps as part of this zero-cost project.** The working project runs locally and requires no AWS resources.

## Cost warning

AWS Free Tier is conditional and is not a guarantee of ₹0. Storage, API requests, logs, query scans, data transfer, networking, and resources left running can incur charges. Pricing and Free Tier terms change. This project deliberately does not call AWS APIs or create infrastructure.

To preserve zero AWS spend for this project:
- Do not create S3 buckets, Lambda functions, Glue crawlers, Athena workgroups, IAM roles or other AWS resources.
- Do not assume a budget alert blocks or prevents charges.
- Do not add AWS credentials to the repository.
- Demonstrate the local app and use the AWS architecture diagram for portfolio discussion.

## Future deployment sequence (read for learning, not now)

If you later choose to deploy and accept possible charges, first review current AWS pricing and account-specific Free Tier terms. A possible sequence is:
1. Create an S3 bucket with Block Public Access and default encryption enabled.
2. Separate source files under `raw/` and transformed files under `curated/`.
3. Create a least-privilege Lambda execution role.
4. Package the transformation function and dependencies.
5. Configure S3 ObjectCreated notification for `raw/`; write output only to `curated/` to avoid recursive triggers.
6. Define or crawl the curated dataset in Glue.
7. Configure Athena query results storage and test with small datasets.
8. Export results to a BI tool.
9. Monitor storage, invocations, logs, bytes scanned and billing.
10. Delete resources and objects when finished, after checking dependencies and retained data.

## Production security checklist

- Block public access to buckets; encrypt data at rest and in transit.
- Apply least-privilege IAM; never use root credentials in an application.
- Never commit keys, secrets or passwords.
- Validate file size, schema, encoding and contents.
- Make processing idempotent and handle retries/dead-letter events.
- Set appropriate Lambda timeout, memory and concurrency.
- Configure monitoring and retention while accounting for their cost.

## Interview explanation

"I implemented and tested the analytics pipeline locally with Python, Pandas, SQLite and Streamlit. I documented how its stages map to an AWS serverless data lake using S3, Lambda, Glue and Athena. I did not deploy cloud resources, so this portfolio implementation has no AWS infrastructure or cloud usage charges."
