package cmd

import (
	"fmt"

	"github.com/hmahdiany/ranger/builder"
	"github.com/hmahdiany/ranger/kubecontext"
	"github.com/spf13/cobra"
	"k8s.io/client-go/kubernetes"
)

var (
	Namespace, Objects []string
	cfgFile            string
	clientset          *kubernetes.Clientset
	err                error

	dumpCmd = &cobra.Command{
		Use:   "dump",
		Short: "create dump file",
		Run: func(cmd *cobra.Command, args []string) {

			if len(Namespace) == 0 {
				fmt.Println("Dumping all user defined namespaces")
				ns := builder.ListAllNS()
				fmt.Println(ns)
			} else {
				ns := builder.ListNS(Namespace)
				fmt.Println(ns)
			}
		},
	}
)

func init() {
	dumpCmd.Flags().StringVarP(&cfgFile, "config", "c", "", "kubectl config file to access k8s cluster")
	dumpCmd.Flags().StringSliceVarP(&Namespace, "namespace", "n", []string{}, "user defined namespace list")
	//dumpCmd.Flags().StringSliceVarP(&Objects, "kind", "k", []string{}, "list of kubernetes objects to dump")
	rootCmd.AddCommand(dumpCmd)
}

func initConfig() {
	if cfgFile != "" {
		// Use config file from the flag.
		clientset, err := kubecontext.CreateContext(cfgFile)
		if err != nil {
			panic(err.Error())
		}
		fmt.Println(clientset)
	}
}
