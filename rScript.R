args <- commandArgs(TRUE)
input= args[1]
output=paste(input,".pdf",sep="")
print(input)## preliminary stuff

## species.it=function(input,output,sep=F) #original
species.it=function(sep=F){
   input <- "data/cavebear.txt.9"
   output <- "data/cavebear2.pdf"
   res=vector("list") #list()
   a=read.table(input,head=T,as.is=T) #komplette Datei
   a.new=a #komplette Datei nochmal...!?
   mol=as.numeric(sapply(rownames(a),function(x) substring(strsplit(x,"_")[[1]][1],2,nchar(strsplit(x,"_")[[1]][1])))) #IDs mit (5?), 4,3,2...not sure
   print("mol is:")
   print(mol)
   mol2=rownames(a) #IDs von der Tabelle
   print("mol2 is:")
   print(mol2)
   tot=c() #beim ersten Mal (?) NULL
   print("tot is:")
   print(tot)
   tot[1]=sum(mol) # =1.266.160
   res[[1]]=vector("list") #list() AGAIN...
   res[[1]][[1]]=a.new #komplette Datei/Tabelle, zum dritten Mal...
   ii=1
   while(nrow(a.new)>0 & ii<=3){ #waehrend die Anzahl der Reihen > 0 und ii (wahrscheinlich Anzahl der drei besten Ergebnisse) <=3
     res[[ii+1]]=vector("list")
     cat(ii,"best_species ","\n")
     id=apply(a.new,2,function(x) sum(!is.na(x))) #auf Tabelle a.new, Spalten (2),  prüft für alle Elemente in x, ob es sich um fehlende oder um gültige Werte handelt (also is.NA?)
     #IDs > Ursus_spelaeus: 20340
     #IDs > Home Sapiens: 2018
     #IDs > Tremarctos: 106...
     
     sp=names(which(id==max(id)))
     cat(paste(sp,collaps="\n"))
     mol2=mol2[apply(a.new[,sp,drop=F],1,function(x) sum(!is.na(x))==0)]
     mol=mol[apply(a.new[,sp,drop=F],1,function(x) sum(!is.na(x))==0)]
     #cat(mol,"\n")
     tot[ii+1]=sum(mol) #147.968
     a.new=a.new[apply(a.new[,sp,drop=F],1,function(x) sum(!is.na(x))==0),-which(colnames(a.new) %in% sp)]
     res[[ii+1]][[1]]=a.new
     res[[ii+1]][[2]]=sp #Ursus_spelaeus
     ii=ii+1
     
   }
   if(!sep){
     pdf(output,width=5,height=5*(length(res)-1))
     layout(matrix(1:(length(res)-1),ncol=1))
     n=0
     for(i in 1:(length(res)-1)){
       n=n+1
       image(as.matrix(res[[i]][[1]]),,xlab="sites",ylab="species", main=paste(n," best_species: ",res[[i+1]][[2]],sep=""),sub=paste("Total mach: ",tot[i]-tot[i+1],","," not match:",tot[i+1],sep=""))
       cat("Total mach: ",tot[i]-tot[i+1],"\n"," not mach:",tot[i+1],"\n")
     
#  main=paste(res[[i+1]][[2]],collapse="\n"))
#  main=paste(res[[i+1]][[2]],collapse="\t")

      }
   }

   dev.off()
   ## return(res)
   if(sep){
     for(i in 1:(length(res)-1)){
     pdf(paste(input,"_step",i,".pdf",sep=""),width=5,height=5*(length(res)-1))
     image(as.matrix(res[[i]][[1]]),,xlab="sites",ylab="species",sub=paste("total: ",tot[1]," left:",tot[i+1],sep=""))
     cat("Total mach: ",tot[i]-tot[i+1],"\n"," not mach:",tot[i+1],"\n")
     dev.off()
    }
  }
 }


 


species.it("data/cavebear.txt.9",output)

# files=list.files()
# files=unlist(unique(sapply(files[grep("*table",files)],function(x) if(length(strsplit(x,"table_")[[1]])==1) x)))
# sapply(files,function(x) species.it(x,paste(x,".pdf",sep="")))
