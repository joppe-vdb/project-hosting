#!/bin/bash
# get the vm to join the cluster
export KUBECONFIG=/home/ccs5/cluster/ccs5-cluster.yaml

# get the status of pods in a namespace
# first we get the name of a pod then we get the status and last we get the number of pods running and the status
podstatus=$(kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].ready}{"\t"}{.status.phase}{"\n"}{end}' -n alpha
)

# give output
echo $podstatus
