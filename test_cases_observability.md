# Test Cases: Observability Platform Queries

## Loki (Logs)

| Test | Description |
|------|-------------|
| [100a_loki_historical_logs](tests/llm/fixtures/test_ask_holmes/100a_loki_historical_logs/test_case.yaml) | Loki historical logs |
| [101_loki_historical_logs_pod_deleted](tests/llm/fixtures/test_ask_holmes/101_loki_historical_logs_pod_deleted/test_case.yaml) | Loki logs (pod deleted) |
| [102_loki_label_discovery](tests/llm/fixtures/test_ask_holmes/102_loki_label_discovery/test_case.yaml) | Loki label discovery |
| [102a_loki_logs_transparency](tests/llm/fixtures/test_ask_holmes/102a_loki_logs_transparency/test_case.yaml) | Loki logs transparency |
| [102b_loki_multiple_pods](tests/llm/fixtures/test_ask_holmes/102b_loki_multiple_pods/test_case.yaml) | Loki multiple pods |

## New Relic (Logs, Metrics, Traces)

| Test | Description |
|------|-------------|
| [117_new_relic_tracing](tests/llm/fixtures/test_ask_holmes/117_new_relic_tracing/test_case.yaml) | New Relic tracing |
| [117b_new_relic_block_embed](tests/llm/fixtures/test_ask_holmes/117b_new_relic_block_embed/test_case.yaml) | New Relic block embed |
| [118_new_relic_logs](tests/llm/fixtures/test_ask_holmes/118_new_relic_logs/test_case.yaml) | New Relic logs |
| [119_new_relic_metrics](tests/llm/fixtures/test_ask_holmes/119_new_relic_metrics/test_case.yaml) | New Relic metrics |
| [120_new_relic_traces2](tests/llm/fixtures/test_ask_holmes/120_new_relic_traces2/test_case.yaml) | New Relic traces (variant 2) |
| [121_new_relic_checkout_errors_tracing](tests/llm/fixtures/test_ask_holmes/121_new_relic_checkout_errors_tracing/test_case.yaml) | New Relic checkout errors tracing |
| [122_new_relic_checkout_latency_tracing_rebuild](tests/llm/fixtures/test_ask_holmes/122_new_relic_checkout_latency_tracing_rebuild/test_case.yaml) | New Relic checkout latency rebuild |
| [123_new_relic_checkout_errors_tracing](tests/llm/fixtures/test_ask_holmes/123_new_relic_checkout_errors_tracing/test_case.yaml) | New Relic checkout errors tracing |
| [124a_new_relic_multi_account_account_name](tests/llm/fixtures/test_ask_holmes/124a_new_relic_multi_account_account_name/test_case.yaml) | New Relic multi-account (by name) |
| [124b_new_relic_multi_account_alert_prompt](tests/llm/fixtures/test_ask_holmes/124b_new_relic_multi_account_alert_prompt/test_case.yaml) | New Relic multi-account (alert) |
| [124c_new_relic_multi_account_default](tests/llm/fixtures/test_ask_holmes/124c_new_relic_multi_account_default/test_case.yaml) | New Relic multi-account (default) |

## Grafana (Metrics, Dashboards)

| Test | Description |
|------|-------------|
| [177_grafana_home_dashboard](tests/llm/fixtures/test_ask_holmes/177_grafana_home_dashboard/test_case.yaml) | Grafana home dashboard |
| [178_grafana_search_dashboard_query](tests/llm/fixtures/test_ask_holmes/178_grafana_search_dashboard_query/test_case.yaml) | Grafana search dashboard query |
| [179_grafana_big_dashboard_query](tests/llm/fixtures/test_ask_holmes/179_grafana_big_dashboard_query/test_case.yaml) | Grafana big dashboard query |
| [212_grafana_render_vision](tests/llm/fixtures/test_ask_holmes/212_grafana_render_vision/test_case.yaml) | Grafana render vision |
| [213_grafana_render_spike_detection](tests/llm/fixtures/test_ask_holmes/213_grafana_render_spike_detection/test_case.yaml) | Grafana render spike detection |
| [237_grafana_large_dashboard_spike](tests/llm/fixtures/test_ask_holmes/237_grafana_large_dashboard_spike/test_case.yaml) | Grafana large dashboard spike |

## Coralogix (Logs, Metrics, Traces)

| Test | Description |
|------|-------------|
| [173_coralogix_logs](tests/llm/fixtures/test_ask_holmes/173_coralogix_logs/test_case.yaml) | Coralogix logs |
| [174_coralogix_traces_ad](tests/llm/fixtures/test_ask_holmes/174_coralogix_traces_ad/test_case.yaml) | Coralogix traces |
| [175_coralogix_metrics_frontend](tests/llm/fixtures/test_ask_holmes/175_coralogix_metrics_frontend/test_case.yaml) | Coralogix metrics (frontend) |

## Datadog (Logs, Metrics, Traces)

| Test | Description |
|------|-------------|
| [91a_datadog_metrics_no_k8s](tests/llm/fixtures/test_ask_holmes/91a_datadog_metrics_no_k8s/test_case.yaml) | Datadog metrics (no k8s) |
| [91b_datadog_metrics_pod_exists](tests/llm/fixtures/test_ask_holmes/91b_datadog_metrics_pod_exists/test_case.yaml) | Datadog metrics (pod exists) |
| [91c_datadog_metrics_deployment](tests/llm/fixtures/test_ask_holmes/91c_datadog_metrics_deployment/test_case.yaml) | Datadog metrics (deployment) |
| [91d_datadog_metrics_historical_pod](tests/llm/fixtures/test_ask_holmes/91d_datadog_metrics_historical_pod/test_case.yaml) | Datadog metrics (historical pod) |
| [91e_datadog_custom_metrics](tests/llm/fixtures/test_ask_holmes/91e_datadog_custom_metrics/test_case.yaml) | Datadog custom metrics |
| [91f_datadog_logs_historical_pod](tests/llm/fixtures/test_ask_holmes/91f_datadog_logs_historical_pod/test_case.yaml) | Datadog logs (historical pod) |
| [91g_datadog_metrics_mismatched_pod](tests/llm/fixtures/test_ask_holmes/91g_datadog_metrics_mismatched_pod/test_case.yaml) | Datadog metrics (mismatched pod) |
| [91h_datadog_logs_empty_query_with_url](tests/llm/fixtures/test_ask_holmes/91h_datadog_logs_empty_query_with_url/test_case.yaml) | Datadog logs empty query |
| [91i_datadog_metrics_empty_query_with_url](tests/llm/fixtures/test_ask_holmes/91i_datadog_metrics_empty_query_with_url/test_case.yaml) | Datadog metrics empty query |
| [111_disabled_datadog_traces](tests/llm/fixtures/test_ask_holmes/111_disabled_datadog_traces/test_case.yaml) | Disabled Datadog traces |
| [164_datadog_traces_coupon_code](tests/llm/fixtures/test_ask_holmes/164_datadog_traces_coupon_code/test_case.yaml) | Datadog traces coupon code |

## Elasticsearch / OpenSearch (Logs, Traces)

| Test | Description |
|------|-------------|
| [156_kafka_opensearch_latency](tests/llm/fixtures/test_ask_holmes/156_kafka_opensearch_latency/test_case.yaml) | Kafka OpenSearch latency |
| [183a_elasticsearch_cluster_health](tests/llm/fixtures/test_ask_holmes/183a_elasticsearch_cluster_health/test_case.yaml) | Elasticsearch cluster health |
| [183b_elasticsearch_index_discovery](tests/llm/fixtures/test_ask_holmes/183b_elasticsearch_index_discovery/test_case.yaml) | Elasticsearch index discovery |
| [183c_elasticsearch_log_search](tests/llm/fixtures/test_ask_holmes/183c_elasticsearch_log_search/test_case.yaml) | Elasticsearch log search |
| [183d_elasticsearch_aggregation](tests/llm/fixtures/test_ask_holmes/183d_elasticsearch_aggregation/test_case.yaml) | Elasticsearch aggregation |
| [183e_elasticsearch_field_mappings](tests/llm/fixtures/test_ask_holmes/183e_elasticsearch_field_mappings/test_case.yaml) | Elasticsearch field mappings |
| [183f_elasticsearch_shard_filtering](tests/llm/fixtures/test_ask_holmes/183f_elasticsearch_shard_filtering/test_case.yaml) | Elasticsearch shard filtering |
| [183g_elasticsearch_index_stats](tests/llm/fixtures/test_ask_holmes/183g_elasticsearch_index_stats/test_case.yaml) | Elasticsearch index stats |
| [184_elasticsearch_index_explosion](tests/llm/fixtures/test_ask_holmes/184_elasticsearch_index_explosion/test_case.yaml) | Elasticsearch index explosion |
| [185_elasticsearch_cross_region_search](tests/llm/fixtures/test_ask_holmes/185_elasticsearch_cross_region_search/test_case.yaml) | Elasticsearch cross-region search |
| [186_elasticsearch_shard_explosion](tests/llm/fixtures/test_ask_holmes/186_elasticsearch_shard_explosion/test_case.yaml) | Elasticsearch shard explosion |
| [187_elasticsearch_disk_space](tests/llm/fixtures/test_ask_holmes/187_elasticsearch_disk_space/test_case.yaml) | Elasticsearch disk space |
| [188_elasticsearch_mapping_explosion](tests/llm/fixtures/test_ask_holmes/188_elasticsearch_mapping_explosion/test_case.yaml) | Elasticsearch mapping explosion |
| [189_elasticsearch_timeseries_gap](tests/llm/fixtures/test_ask_holmes/189_elasticsearch_timeseries_gap/test_case.yaml) | Elasticsearch timeseries gap |
| [190_elasticsearch_cross_service_correlation](tests/llm/fixtures/test_ask_holmes/190_elasticsearch_cross_service_correlation/test_case.yaml) | Elasticsearch cross-service correlation |
| [191_elasticsearch_query_profile](tests/llm/fixtures/test_ask_holmes/191_elasticsearch_query_profile/test_case.yaml) | Elasticsearch query profile |
| [193_elasticsearch_large_mapping_search](tests/llm/fixtures/test_ask_holmes/193_elasticsearch_large_mapping_search/test_case.yaml) | Elasticsearch large mapping search |
| [235_elasticsearch_cluster_mismatch](tests/llm/fixtures/test_ask_holmes/235_elasticsearch_cluster_mismatch/test_case.yaml) | Elasticsearch cluster mismatch |
| [245_elasticsearch_trace_large_fields](tests/llm/fixtures/test_ask_holmes/245_elasticsearch_trace_large_fields/test_case.yaml) | Elasticsearch trace large fields |

## Prometheus (Metrics)

| Test | Description |
|------|-------------|
| [124_checkout_latency_prometheus](tests/llm/fixtures/test_ask_holmes/124_checkout_latency_prometheus/test_case.yaml) | Checkout latency Prometheus |
| [159_prometheus_high_cardinality_cpu](tests/llm/fixtures/test_ask_holmes/159_prometheus_high_cardinality_cpu/test_case.yaml) | Prometheus high cardinality CPU |
| [211_prometheus_alerting_rules](tests/llm/fixtures/test_ask_holmes/211_prometheus_alerting_rules/test_case.yaml) | Prometheus alerting rules |
| [233_compaction_prometheus_data](tests/llm/fixtures/test_ask_holmes/233_compaction_prometheus_data/test_case.yaml) | Compaction Prometheus data |

## Tempo (Traces)

| Test | Description |
|------|-------------|
| [35_tempo](tests/llm/fixtures/test_ask_holmes/35_tempo/test_case.yaml) | Tempo traces |
| [114_checkout_latency_tracing_rebuild](tests/llm/fixtures/test_ask_holmes/114_checkout_latency_tracing_rebuild/test_case.yaml) | Checkout latency tracing |
| [115_checkout_errors_tracing](tests/llm/fixtures/test_ask_holmes/115_checkout_errors_tracing/test_case.yaml) | Checkout errors tracing |

## Summary

| Platform | Count |
|----------|-------|
| Loki | 5 |
| New Relic | 11 |
| Grafana | 6 |
| Coralogix | 3 |
| Datadog | 11 |
| Elasticsearch / OpenSearch | 19 |
| Prometheus | 4 |
| Tempo | 3 |
| **Total** | **62** |
