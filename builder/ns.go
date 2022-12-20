package builder

import "fmt"

func ListAllNS() []string {
	allns := []string{
		"gitlab",
		"ingress-nginx",
		"websit",
	}

	return allns
}
func ListNS(ns []string) []string {
	fmt.Println("I am ListNs function")
	return ns
}

func Config(path string) string {
	fmt.Println("I am ListNs function")
	return path
}
