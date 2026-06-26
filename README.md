# Enterprise Data Lakehouse Platform

Enterprise-grade data lakehouse platform built with Terraform, AWS S3, Delta Lake, Apache Spark, and GitHub Actions CI/CD pipeline.

## Architecture
GitHub Actions CI/CD -> Terraform -> AWS S3 (Raw, Bronze, Silver, Gold) -> Apache Spark + Delta Lake -> Power BI

## Tech Stack
- Terraform (Infrastructure as Code)
- AWS (S3, IAM, EC2, Glue, EMR)
- Apache Spark + Delta Lake
- Apache Airflow (orchestration)
- dbt (transformations)
- GitHub Actions (CI/CD)
- Docker (containerization)
- Python

## Features
- Medallion architecture (Raw, Bronze, Silver, Gold layers)
- Infrastructure as Code with Terraform
- Automated CI/CD with GitHub Actions
- S3 versioning enabled on all layers
- IAM role-based access control
- Data governance and lineage tracking

## How to Run
cd terraform
terraform init
terraform plan
terraform apply

## Status
Phase 1 Complete: Terraform + AWS Infrastructure
Phase 2 Pending: Apache Spark + Delta Lake
Phase 3 Pending: Apache Iceberg + Unity Catalog
Phase 4 Pending: DataHub + Data Lineage
Phase 5 Pending: dbt + Data Quality

## dbt Transformations
dbt models implemented in Financial Data Pipeline project:
- Staging models: Raw data cleaning and validation
- Mart models: Business-ready analytical datasets
- Data lineage: Full column-level lineage tracking
- Tests: Automated quality validation

See: github.com/meghashyamkomari-prog/financial-data-pipeline

## dbt Transformations
dbt models implemented in Financial Data Pipeline project:
- Staging models: Raw data cleaning and validation
- Mart models: Business-ready analytical datasets
- Data lineage: Full column-level lineage tracking
- Tests: Automated quality validation

See: github.com/meghashyamkomari-prog/financial-data-pipeline
