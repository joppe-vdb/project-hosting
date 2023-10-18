#!/bin/bash
# get the vm to join the cluster
export KUBECONFIG=/home/ccs5/cluster/ccs5-cluster.yaml

# delete everything that has to do with namepace of the project
kubectl delete namespace $1