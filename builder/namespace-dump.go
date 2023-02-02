package builder

import (
	"context"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

type AllNsList v1.NamespaceList

type UserInputNsList map[string]string

func DumpAllNamespaces(clientset *kubernetes.Clientset) {

	a := AllNsList{}

	namesapceList, err := clientset.CoreV1().Namespaces().List(context.TODO(), metav1.ListOptions{})

	if err != nil {
		panic(err.Error())
	}

	a.StoreYamlFile(namesapceList)
}

func DumpUserInputNamespaces(clientset *kubernetes.Clientset, namesapceList []string) {

	a := UserInputNsList{}

	for i := 0; i < len(namesapceList); i++ {
		ns, err := clientset.CoreV1().Namespaces().Get(context.TODO(), namesapceList[i], metav1.GetOptions{})

		if err != nil {
			panic(err.Error())
		}

		a.StoreYamlFile(ns.Annotations, ns.Name)
	}

}
