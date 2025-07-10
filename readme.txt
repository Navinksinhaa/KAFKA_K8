apply the terraform script to create the namespace and install Strimzi Kafka Operator:

-terraform init
-terraform apply --auto-approve
-kubectl -n kafka get po

we create the Kafka cluster by applying the following yaml file with the command :
- kubectl apply -n kafka -f kafka-persistent.yaml

-kubectl -n kafka apply -f kafka/kafka-topic.yaml

To produce some events to our topic, we can run the following command:

-echo "Hello KafkaOnKubernetes" | kubectl -n kafka exec -i my-cluster-kafka-0 -c kafka -- \
    bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic

To test consuming this event, we run:
kubectl -n kafka exec -i my-cluster-kafka-0 -c kafka -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning

Setting-up Prometheus
-curl -s https://raw.githubusercontent.com/coreos/prometheus-operator/master/bundle.yaml \
> prometheus-operator-deployment.yaml
Then we update the namespace with our observability namespace:
sed -E -i '/[[:space:]]*namespace: [a-zA-Z0–9-]*$/s/namespace:[[:space:]]*[a-zA-Z0–9-]*$/namespace: observability/' prometheus-operator-deployment.yaml

Then, deploy the Prometheus Operator:
kubectl -n observability create -f prometheus-operator-deployment.yaml

Now that we have the operator up and running, we need to create the Prometheus server and configure it to watch for Strimzi CRDs in the kafka namespace.

Then we create the Prometheus object and configure it to look for all pods with the labels app: strimzi
kubectl -n observability create -f strimzi-pod-monitor.yaml

Note that for this to work, we also need the corresponding ServiceAccount, and RBAC objects as follow:

kubectl apply -f kafka-metrics.yaml -n kafka


Now we need to install Grafana using the grafana.yaml file then configure our Prometheus as a data source

kubectl -n observability apply -f grafana-install/grafana.yaml
