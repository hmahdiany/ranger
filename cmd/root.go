package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "ranger",
	Short: "ranger - a simple CLI to dump k8s manifests",
	Long: `ranger is a super fancy CLI (kidding)
One can use to dump all related manifests in a k8s namesapce`,
	Run: func(cmd *cobra.Command, args []string) {

	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Whoops. There was an error while executing ranger '%s'", err)
		os.Exit(1)
	}
}
