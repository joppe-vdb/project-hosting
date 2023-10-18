# get the vm to join the cluster
export KUBECONFIG=/home/ccs5/cluster/ccs5-cluster.yaml

# move to correct folder
cd /home/ccs5/projects/$1/config

# change the deployment file
kubectl apply -f $1-$2-deployment.yaml --validate=false # deployment
