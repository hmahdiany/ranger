package cmd

import (
	"fmt"

	"github.com/hmahdiany/ranger/builder"
	"github.com/hmahdiany/ranger/kubecontext"
	"github.com/spf13/cobra"
	"k8s.io/client-go/kubernetes"
)

var (
	Namespaces, Objects []string
	cfgFile             string
	clientset           *kubernetes.Clientset
	err                 error

	dumpCmd = &cobra.Command{
		Use:   "dump",
		Short: "create dump file",
		Run: func(cmd *cobra.Command, args []string) {

			// Use config file from the flag.
			clientset, err := kubecontext.CreateContext(cfgFile)
			if err != nil {
				panic(err.Error())
			}

			// make a decision based on user input namespace list
			if len(Namespaces) == 0 {
				fmt.Println("Dumping all user defined namespaces")
				builder.DumpAllNamespaces(clientset)
			} else {
				fmt.Printf("Dumping these namespace(s): %v\n", Namespaces)
				builder.DumpUserInputNamespaces(clientset, Namespaces)
			}
		},
	}
)

func init() {
	dumpCmd.Flags().StringVarP(&cfgFile, "config", "c", "", "kubectl config file to access k8s cluster")
	dumpCmd.Flags().StringSliceVarP(&Namespaces, "namespace", "n", []string{}, "user defined comma seperated namespace list")
	//dumpCmd.Flags().StringSliceVarP(&Objects, "kind", "k", []string{}, "list of kubernetes objects to dump")
	rootCmd.AddCommand(dumpCmd)
}
