package builder

import (
	"context"
	"fmt"

	"github.com/hmahdiany/ranger/kubecontext"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func ListAllNS(kubeconfig string) {

	// Use config file from the flag.
	clientset, err := kubecontext.CreateContext(kubeconfig)
	if err != nil {
		panic(err.Error())
	}

	namesapceList, err := clientset.CoreV1().Namespaces().List(context.TODO(), metav1.ListOptions{})

	if err != nil {
		panic(err.Error())
	}

	//fmt.Println(namesapceList.ListMeta)
	StoreYamlFile(namesapceList)
}

func ListNS(ns []string) []string {
	fmt.Println("I am ListNs function")
	return ns
}

func Config(path string) string {
	fmt.Println("I am ListNs function")
	return path
}
