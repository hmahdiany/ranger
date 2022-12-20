package kubecontext

import (
	"fmt"
	"path/filepath"

	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
)

func CreateContext(kubeconfig string) (*kubernetes.Clientset, error) {
	if kubeconfig == "" {
		fmt.Println("using default path")
		kubeconfig = filepath.Join(homedir.HomeDir(), ".kube", "config")

		// use the current context in kubeconfig
		config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
		if err != nil {
			panic(err.Error())
		}

		// create the clientset
		clientset, err := kubernetes.NewForConfig(config)

		return clientset, err
	}
}
