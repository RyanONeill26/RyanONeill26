        @Load in an 8-bit number to generate a 12-bit hamming number
        
        LDR	r0, =0xac
        
        AND	R2, R0, #0x1		@ Clear all bits apart from d0
        MOV	R1, R2, LSL #2		@ Align data bit d0
    		
        AND	R2, R0, #0xE		@ Clear all bits apart from d1, d2, & d3
        ORR	R1, R1, R2, LSL #3	@ Align data bits d1, d2 & d3 and combine with d0
    		
        AND	R2, R0, #0xF0		@ Clear all bits apart from d3-d7
        ORR	R1, R1, R2, LSL #4	@ Align data bits d4-d7 and combine with d0-d3
    		
        @ We now have a 12-bit value in R0 with empty (0) check bits in
        @ the correct positions
    		
    	
        @Generate check bit c0
    		
        EOR	R2, R1, R1, LSR #2	@ Generate c0 parity bit using parity tree
        EOR	R2, R2, R2, LSR #4	@ second iteration 
        EOR	R2, R2, R2, LSR #8	@ final iteration
    		
        AND	R2, R2, #0x1		@ Clear all but check bit c0
        ORR	R1, R1, R2		@ Combine check bit c0 with result
    		
        @Generate check bit c1
      		
        EOR	R2, R1, R1, LSR #1	@ Generate c1 parity bit using parity tree
        EOR	R2, R2, R2, LSR #4	@ second iteration 
        EOR	R2, R2, R2, LSR #8	@ final iteration
    		
        AND	R2, R2, #0x2		@ Clear all but check bit c1
        ORR	R1, R1, R2		@ Combine check bit c1 with result
    		
        @Generate check bit c3
    		
        EOR	R2, R1, R1, LSR #1	@ Generate c2 parity bit using parity tree
        EOR	R2, R2, R2, LSR #2	@ second iteration 
        EOR	R2, R2, R2, LSR #8	@ final iteration
    		
        AND	R2, R2, #0x8		@ Clear all but check bit c2
        ORR	R1, R1, R2		@ Combine check bit c2 with result	
    		
        @Generate check bit c7
    		
        EOR	R2, R1, R1, LSR #1	@ Generate c3 parity bit using parity tree
        EOR	R2, R2, R2, LSR #2	@ second iteration 
        EOR	R2, R2, R2, LSR #4	@ final iteration
    		
        AND	R2, R2, #0x80		@ Clear all but check bit c3
        ORR	R1, R1, R2		@ Combine check bit c3 with result

        MOV     R0, R1		
        @We now have a 12-bit value with Hamming code check bits in R0
    		
        @Create an artificial "error" in the encoded value by flipping a single bit
    		
        EOR	R0, R0, #0x100		@ Flip bit 8 to test

        @Clear bits c0, c1, c3, c7
        
        LDR R3, =0xF74
        AND R3, R0, R3
                        
        @Generate check bit c0
                    
        EOR    R2, R3, R3, LSR #2    @ Generate c0 parity bit using parity tree
        EOR    R2, R2, R2, LSR #4    @ second iteration 
        EOR    R2, R2, R2, LSR #8    @ final iteration
                    
        AND    R2, R2, #0x1        @ Clear all but check bit c0
        ORR    R3, R3, R2        @ Combine check bit c0 with result
                  
       @Generate check bit c1
                  
       EOR    R2, R3, R3, LSR #1    @ Generate c1 parity bit using parity tree
       EOR    R2, R2, R2, LSR #4    @ second iteration 
       EOR    R2, R2, R2, LSR #8    @ final iteration
                  
       AND    R2, R2, #0x2        @ Clear all but check bit c1
       ORR    R3, R3, R2        @ Combine check bit c1 with result
                  
       @Generate check bit c3
                  
       EOR    R2, R3, R3, LSR #1    @ Generate c2 parity bit using parity tree
       EOR    R2, R2, R2, LSR #2    @ second iteration 
       EOR    R2, R2, R2, LSR #8    @ final iteration
                  
       AND    R2, R2, #0x8        @ Clear all but check bit c2
       ORR    R3, R3, R2        @ Combine check bit c2 with result    
                  
       @Generate check bit c7
                  
       EOR    R2, R3, R3, LSR #1    @ Generate c3 parity bit using parity tree
       EOR    R2, R2, R2, LSR #2    @ second iteration 
       EOR    R2, R2, R2, LSR #4    @ final iteration
                  
       AND    R2, R2, #0x80        @ Clear all but check bit c3
       ORR    R3, R3, R2        @ Combine check bit c3 with result
              
       @Recalculated value of 12 bit number in R3     
                  
       @Compare the original value and the recalculated value using exclusive-OR
       EOR R1, R0, R3
              
              
       @Isolate the results of the EOR operation to result in a 4-bit calculation
              
       @Clearing all bits apart from c7 and shifting bit 4 positions right
       LDR R4, =0X80
       AND R4, R4, R1
       MOV R4, R4, LSR #4
              
       @Clearing all bits apart from c3 and shifting the 3rd bit 1 position right
       LDR R5, =0X8
       AND R5, R5, R1
       MOV R5, R5, LSR #1
              
       @Clearing all bits apart from c0 and c1  
       LDR R6, =0X3
       AND R6, R6, R1
              
              
       @Adding the 3 registers together 
       ADD R1, R4, R5
       ADD R1, R1, R6
        
       @ 4 bit number now in R1 that shows the position of the error bit
              
       @Subtracting 1 from R0 to determine the bit position of the error(binary starts at 0)
       SUB R1, R1, #0X1
              
       @Moving to the location of the error bit
       LDR R7, =0X1
       MOV R7, R7, LSL R1
              
       @Flips the error bit of R1 and stores it in R0
       EOR R0, R0, R7

       @Clear the check bits and shift the remaining bits to make
       @The original 8 bit number before hamming code

       @Clearing c7
       AND    R1, R0, #0xf00
       MOV    R1,R1, LSR #4

       AND    R2, R0, #0x70
       MOV     R2,R2, LSR #3

       AND    R3, R0, #0x4
       MOV    R3,R3, LSR #2
       LDR    R0, =0x0
    
       ORR     R0,R1
       ORR     R0,R2
       ORR     R0,R3
       
       @Now ac is once again in R0
