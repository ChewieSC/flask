args <- commandArgs(TRUE)
input= args[1]
output=paste(input,".pdf",sep="")
print(input)
species.it=function(input,output,sep=F){
   res=vector("list")
   a=read.table(input,head=T,as.is=T)
   a.new=a
   mol=as.numeric(sapply(rownames(a),function(x) substring(strsplit(x,"_")[[1]][1],2,nchar(strsplit(x,"_")[[1]][1]))))
   mol2=rownames(a)
   tot=c()
   tot[1]=sum(mol)
   res[[1]]=vector("list")
   res[[1]][[1]]=a.new
   ii=1
   while(nrow(a.new)>0 & ii<=3){
     res[[ii+1]]=vector("list")
     cat(ii,"best_species ","\n")
     id=apply(a.new,2,function(x) sum(!is.na(x)))
     sp=names(which(id==max(id)))
     cat(paste(sp,collaps="\n"))
     mol2=mol2[apply(a.new[,sp,drop=F],1,function(x) sum(!is.na(x))==0)]
     mol=mol[apply(a.new[,sp,drop=F],1,function(x) sum(!is.na(x))==0)]
     #cat(mol,"\n")
     tot[ii+1]=sum(mol)
     a.new=a.new[apply(a.new[,sp,drop=F],1,function(x) sum(!is.na(x))==0),-which(colnames(a.new) %in% sp)]
     res[[ii+1]][[1]]=a.new
     res[[ii+1]][[2]]=sp
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
 


species.it(input,output)

# files=list.files()
# files=unlist(unique(sapply(files[grep("*table",files)],function(x) if(length(strsplit(x,"table_")[[1]])==1) x)))
# sapply(files,function(x) species.it(x,paste(x,".pdf",sep="")))