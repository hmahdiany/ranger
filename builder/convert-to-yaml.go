package builder

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"

	"github.com/ghodss/yaml"
	v1 "k8s.io/api/core/v1"
)

func StoreYamlFile(namspaceList *v1.NamespaceList) {

	// iterate through namespace list
	for i := 0; i < len(namspaceList.Items); i++ {

		// skip namespaces which starts with kube-
		re, _ := regexp.Compile("kube-.*")
		match := re.FindString(namspaceList.Items[i].Name)
		if match != "" {
			fmt.Printf("skip dumping %v namespace\n", match)
			continue
		}

		rawData, err := yaml.Marshal(namspaceList.Items[i].ObjectMeta.Annotations)
		if err != nil {
			log.Fatal(err)
		}

		NsDump := bytes.TrimPrefix(rawData, []byte("kubectl.kubernetes.io/last-applied-configuration: |"))

		yamlData, err := yaml.JSONToYAML(NsDump)
		if err != nil {
			log.Fatal(err)
		}

		// create dump directy if it is not exists
		if _, err := os.Stat("dump"); os.IsNotExist(err) {
			fmt.Println("dump directory does not exists, creating dump directory")
			err := os.Mkdir("dump", 0755)
			if err != nil {
				log.Fatal(err)
			}
		}

		// create a subdirectory in dump directory for each namespace
		if _, err := os.Stat(filepath.Join("dump", namspaceList.Items[i].Name)); os.IsNotExist(err) {
			fmt.Printf("creating subdirectory dump/%s\n", namspaceList.Items[i].Name)
			err = os.Mkdir(filepath.Join("dump", namspaceList.Items[i].Name), 0755)
			if err != nil {
				log.Fatal(err)
			}
		}

		// store dump file
		os.WriteFile(filepath.Join("dump", namspaceList.Items[i].Name, "ns.yaml"), yamlData, 0644)
	}
}
