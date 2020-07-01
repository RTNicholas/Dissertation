####
#
# 20/02/20
#
# Matrix Functions
#
#
#Guide: Matrix
#
#   A = [[a00,a01,...,a0(n-1)],.....,[a(m-1)0,a(m-1)0,...,a(m-1)(n-1)]], 
#   A[m-1][n-1] =a(m-1)(n-1)
#----------------------------------------------------------------------
# Some (m by n) matrix A is defined as a list of lists, where the length
# of A is m and the length of the rows of A is n. To reference an element
# of A then it will be the m-1th and n-1th element due to the 0 start of
# python iterative counting. 
#----------------------------------------------------------------------
# Example Matrices
A = [[1]] 
B = [[1,2],[2,1]]
E = [[1,2],[1]]
D = [[1],[2,1]]
F = [[1,2,3],[4,5,6]]
#------------------------

#=================== Matrix Tests and Constructions ===================

# Matrix Size Test
def validity(A):# Confirm input is a rectangular matrix
    #Does not check input is List

    for i in range(len(A)): #For each row
        if len(A[0]) != len(A[i-1]): #Are the number of columns consistent?
            print("Error Matrix", A, "Invalid")  #Erorr if not
            return 0  #Return 0 
            break
        
        elif i+1 == len(A): #If all columns are consistent 
            return 1 #Return 1
            
#Square Validity:
def sqaure(A):
    #Does not check input is List
    #Test input is square
    for i in range(len(A)): #For each row
        #Are the number of columns consistent and equal to number of rows?
        if len(A[0]) != len(A[i-1]) and len(A[i-1]) == len(A): 
            print("Error Matrix", A, "Not square") #Erorr if not
            return 0 #Return 0 
            break
        elif i+1 == len(A): #If all columns are consistent 
            return 1 #Return 1

#Construct m by n matrix with dummy variables
#Useful for other functions
def mBuild(m,n):
    A=[]
    for i in range(m): #Make m rows
        A.append([])
        for j in range(n): #Make n columns
            a = ("a",str(i),str(j)); #Fill each with "a" & m & n
            A[i].append("".join(a))
    return A #Return the dummy matrix

#Identity
def Identity(n): #Build identity of size n

    I = mBuild(n,n) #Build sqaure dummy matrix n by n
    for i in range(n): #For each row
        for j in range(n): #For each column
            if i==j: #Put a 1 on the diagonal
                I[i][j] = 1
            else: #Put 0 everywhere else
                I[i][j] = 0
    return I #Return Matrix

#Display Matrix
#Second best Function
def mDisplay(A): # Display matrix in python in a nicer format
    for m in range(len(A)): #Print each row on seperate line
        print(A[m])                        

#=================== Matrix Arithmetic ===================

# Matrix Transpose 
def T(A): # Transpose of A 
    if validity(A) == 1: #Test validity
        
        B = mBuild(len(A[0]),len(A)) # Build Matrix n by m 
        for m in range(len(A)): # For every Row in A 
            for n in range(len(A[0])): #For every Column in A
                B[n][m] = A[m][n] # Rows become columns and columns become rows
        return B # Return transposed matrix


#Matrix addition
def mAdd(A,B): # Add 2 Matrices A + B
    if len(A)!=len(B) or len(A[0])!=len(B[0]): #Test compatible size
        print("Matrix sizes incompatible") #If not compatible then error
        return
    
    if validity(A) == 1 and validity(B) == 1: #Test validity
        C = mBuild(len(A),len(A[0]))
        for m in range(len(A)): #For each row
            for n in range(len(A[m])): #for each column
                C[m][n] = A[m][n]+B[m][n] #Add each element  
        return C #Return resultant matrix
    
#Dot product of Vectors, v =[v0,v1,..,vn], v[n]=vn,
#   a vector can be a matrix by using [v] 
def vDot(v,u):
    #No formal validity Test yet, Assumes Vector is row
    if len(v) != len(u): #Vectors must be same size
        print("Error") #Else error
        return
    x=0
    for i in range(len(v)): #For each element
        #Multiply corespoding element in other vector 
            x=x+v[i]*u[i] #Add as to total sum
    return x #Return resultant number
    

#Matrix Multiplication
#For A (m1 by n1), B (m2 by n2) then n1 = m2
def mDot(A,B): # Multiply 2 Matrices A*B
    if len(A[0])!=len(B): #Test compatible size
        print("Matrix sizes incompatible")
        return
    
    if validity(A) == 1 and validity(B) == 1: #Test validity
        C = mBuild(len(A),len(B[0])) #Build dummy resultant matrix (m1 by n2)
        for m in range(len(A)): #for each row of A
            for n in range(len(B[0])): #for each column of B
                C[m][n] = vDot(A[m],T(B)[n]) # Element is equal to the dot product of row A with Column B
                #Note: Transpose allows use B columns to be used as rows, easier for code
        return  C #Return Resultant matrix

#Scalar Multiplication
def mCross(x,A): #Multiply matrix by scalar x
    
    B = mBuild(len(A),len(A[0])) #Build matrix with m by n of input A 
    for m in range(len(A)): #For each row of A
        for n in range(len(A[0])): #For each column of A 
            B[m][n] = A[m][n]*x #Each element is equal to element of A time scalar x
    return B #Return resultant B 

#=================== Matrix Augmentation ===================

#Combine 2 matrices of same Row size into 1 
def mComb(A,B): #C = [A|B]
    if len(A) != len(B): #Matrices must have same number of rows
        print("Error matrices not same size")
        return
    #To combine by matching columns, use transpose
    
    if validity(A) == 1 and validity(B) == 1: #Test validity   
        C = mBuild(len(A),len(A[0])+len(B[0])) # Build m by n1 +n2 matrix
        for m in range(len(A)): #for each row 
            for n in range(len(A[0])): #for column of A
                C[m][n] =  A[m][n] # Element of C becomes A
            for i in range(len(B[0])): #for each column of B 
                C[m][len(A[0])+i] = B[m][i] #Element of C+Column size of A becomes elem of B 
        return C #Return augmented matrix

#Produce submatrix by specifying Rows (m) and Columns (n) and starting element (i,j) (Left Bias)
def mDecomb(A,m,n,i,j): 
    if validity(A) == 1: #Test validity
        C = mBuild(m,n)
        for x in range(m): #for each row specified
            for y in range(n): #for each column specfied
                C[x][y] = A[i+x][j+y] #Starting from specfied element, obtain sub matrix
        return C #Return Submatrix
    
    

#=================== Python Conversion Codes ===================

      
def mTex(A): #Convert matrix for latex
    L = []
    for m in range(len(A)): #For each row of A
        for n in range(len(A[0])): #For each col of A
            L.append(str(A[m][n])) #Append element to list
            if n != len(A[0])-1: #if not end of row add &
                L.append("&")
        if m != len(A)-1: #If end of row add \\
            L.append("\\")
    return "".join(L) #return string of latex converted matrix
        
    




            
            
