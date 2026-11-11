# Reading infrastructure-as-code resource types

Infrastructure-as-code (IaC) files name each resource with a type, such as `aws_db_instance`.
This page shows how to turn any type into an icon ref. The examples are samples of the
pattern, not a full list. Most types won't be listed here: work them out with the steps.

## 1. Find the vendor and the service words

| Format | Example type | Vendor | Service words |
| --- | --- | --- | --- |
| Terraform | `aws_db_instance` | prefix `aws_` → `aws` | `db instance` |
| Terraform | `azurerm_key_vault` | prefix `azurerm_` → `azure` | `key vault` |
| Terraform | `google_sql_database_instance` | prefix `google_` → `gcp` | `sql database instance` |
| Pulumi | `aws.rds.Instance` | first part → `aws` | the middle part, `rds`, names the service |
| Pulumi | `azure-native.storage.StorageAccount` | `azure-native` → `azure` | `storage account` |
| Pulumi | `gcp.cloudrun.Service` | `gcp` | `cloudrun` |
| CloudFormation | `AWS::RDS::DBInstance` | `AWS` → `aws` | the middle part, `RDS` |
| Bicep or ARM | `Microsoft.Sql/servers` | `Microsoft.` → `azure` | `Sql`, then `servers` |

The service part matters most. The last part (`Instance`, `servers`, `DBInstance`) often just
says what kind of object it is.

## 2. Turn the service words into a ref

1. If the type matches an example in the table below, use that ref. The examples are written
   as Terraform types, but they apply to the same service in any format:
   `AWS::DynamoDB::Table` and `aws.dynamodb.Table` use the `aws_dynamodb_table` row.
2. Otherwise, say the service by its product name. `db instance` on AWS is Amazon RDS, so try
   `aws:amazon-rds`. `cloudrun` on Google Cloud is Cloud Run, so try `gcp:cloud-run`.
   Apply the import rules for names: lowercase, words joined with `-`, AWS names starting with
   `amazon-` or `aws-` as the product does.
3. Look the ref up as usual (aliases, then the icon files). Vendors often use short or odd
   icon names (`aws:amazon-efs`, `azure:cache-redis`), so a miss here is normal. Then search the
   icon files for `"ref":"<vendor>:` lines holding the main service word (`redis`, `postgres`,
   `kubernetes`, `queue`), and pick the closest name. Search for the ref text only, since each
   line is very long.
4. If nothing fits, use the matching `open:kind-*` icon. Those are shipped in this skill's
   `icons/` folder, not in the imported icons folder.

## 3. Decide what becomes a node

- **Groups:** networks and resource groups (`aws_vpc`, `aws_subnet`, `azurerm_resource_group`,
  `azurerm_virtual_network`, `google_compute_network`). Draw them as containers. Skip a group
  that would hold nothing.
- **Services:** resources a person would point to on a diagram, such as databases, functions,
  clusters, queues, buckets and load balancers.
- **Leave out** settings that only configure another resource: policies and policy
  attachments, role bindings, security group rules, route table associations, IAM (Identity
  and Access Management) members, DNS records, bucket settings such as
  `aws_s3_bucket_versioning`, logging and monitoring setup (log groups, alarms, dashboards,
  diagnostic settings), and random or local helpers. Fold them into the resource they set up.
  Draw a monitoring service as a node only when the person asks about monitoring.
- **Edges:** one resource naming another (`aws_lambda_function.api.arn`, `dependsOn`,
  `resourceId(...)`). Draw the arrow in the direction data or calls flow, not the direction of
  the reference, when you can tell. A resource that only links two others
  (`aws_lambda_event_source_mapping`, `AWS::Lambda::EventSourceMapping`, a subscription or a
  trigger) becomes one arrow between them, not a node. Draw one arrow per pair, even when
  several references join the same two resources.
- **Direction:** a queue, stream or topic that feeds a function points to the function. A
  function or app points to the database, bucket or queue it writes to or reads from. When
  the only clue is a setting such as an environment variable, point from the resource that
  holds the setting to the one it names.

## Examples

These cover common types and the cases where the type name and the icon name differ.

| Type | Ref |
| --- | --- |
| `aws_db_instance`, `aws_rds_cluster` | `aws:amazon-rds` |
| `aws_s3_bucket` | `aws:amazon-simple-storage-service` |
| `aws_lambda_function` | `aws:aws-lambda` |
| `aws_instance` | `aws:amazon-ec2` |
| `aws_lb`, `aws_alb`, `aws_elb` | `aws:elastic-load-balancing` |
| `aws_vpc` | `aws:virtual-private-cloud-vpc` (group) |
| `aws_subnet` | `aws:private-subnet` or `aws:public-subnet` (group) |
| `aws_dynamodb_table` | `aws:amazon-dynamodb` |
| `aws_api_gateway_rest_api`, `aws_apigatewayv2_api` | `aws:amazon-api-gateway` |
| `aws_sqs_queue` | `aws:amazon-simple-queue-service` |
| `aws_sns_topic` | `aws:amazon-simple-notification-service` |
| `aws_cloudfront_distribution` | `aws:amazon-cloudfront` |
| `aws_route53_zone` | `aws:amazon-route-53` |
| `aws_eks_cluster` | `aws:amazon-elastic-kubernetes-service` |
| `aws_ecs_cluster`, `aws_ecs_service` | `aws:amazon-elastic-container-service` |
| `aws_elasticache_cluster` | `aws:amazon-elasticache` |
| `aws_sfn_state_machine` | `aws:aws-step-functions` |
| `aws_cloudwatch_event_rule` | `aws:amazon-eventbridge` |
| `aws_cognito_user_pool` | `aws:amazon-cognito` |
| `azurerm_resource_group` | `azure:resource-groups` (group) |
| `azurerm_virtual_network` | `azure:virtual-networks` (group) |
| `azurerm_linux_virtual_machine`, `azurerm_windows_virtual_machine` | `azure:virtual-machine` |
| `azurerm_storage_account` | `azure:storage-accounts` |
| `azurerm_mssql_server` | `azure:sql-server` |
| `azurerm_mssql_database` | `azure:sql-database` |
| `azurerm_linux_web_app`, `azurerm_service_plan` | `azure:app-services` |
| `azurerm_linux_function_app` | `azure:function-apps` |
| `azurerm_kubernetes_cluster` | `azure:kubernetes-services` |
| `azurerm_key_vault` | `azure:key-vaults` |
| `azurerm_cosmosdb_account` | `azure:cosmos-db` |
| `azurerm_servicebus_namespace` | `azure:service-bus` |
| `azurerm_container_app_environment` | `azure:container-apps-environments` |
| `azurerm_cdn_frontdoor_profile` | `azure:front-door-and-cdn-profiles` |
| `google_compute_instance` | `gcp:compute-engine` |
| `google_compute_network` | `gcp:virtual-private-cloud` (group) |
| `google_storage_bucket` | `gcp:cloud-storage` |
| `google_sql_database_instance` | `gcp:cloud-sql` |
| `google_cloud_run_v2_service` | `gcp:cloud-run` |
| `google_cloudfunctions2_function` | `gcp:cloud-functions` |
| `google_container_cluster` | `gcp:google-kubernetes-engine` |
| `google_bigquery_dataset` | `gcp:big-query` |
| `google_redis_instance` | `gcp:memorystore` |
| `google_pubsub_topic` | none in the current set: use `open:kind-other` |
