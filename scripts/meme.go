/**
    * @author EliasDH Team
    * @see https://eliasdh.com
    * @since 01/01/2025
**/

package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	rand.Seed(time.Now().UnixNano())
	IQ := rand.Intn(200)
	fmt.Println("Your IQ is:", IQ)
	fmt.Println(meme(IQ))
}

func meme(IQ int) string {
	if (IQ <= 100)
		return "You are not welcome here";
	else if (IQ > 100)
		return "You are welcome here";
}