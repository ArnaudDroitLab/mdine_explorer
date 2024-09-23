import pandas as pd

def get_separate_data(info_current_file):
    if info_current_file["phenotype_column"]==None:
        return None
    else:
        df_init=get_df_file(info_current_file)
        df_taxa=get_df_taxa(info_current_file,"df_taxa")
        df_covariates=get_df_covariates(info_current_file,"reduced")

        df_taxa_1=df_taxa[df_init[info_current_file["phenotype_column"]]==0]
        df_taxa_2=df_taxa[df_init[info_current_file["phenotype_column"]]==1]
        df_covariates_1=df_covariates[df_init[info_current_file["phenotype_column"]]==0]
        df_covariates_2=df_covariates[df_init[info_current_file["phenotype_column"]]==1]
        return [df_covariates_1,df_taxa_1],[df_covariates_2,df_taxa_2]


def get_df_taxa(info_current_file,type_output):
    start_taxa=info_current_file["taxa_start"]
    end_taxa=info_current_file["taxa_end"]

    #No filters
    df_total=get_df_file(info_current_file).iloc[:,start_taxa-1:end_taxa]

    reference_taxa=info_current_file["reference_taxa"]

    #Remove ref column to apply filter
    cols = [col for col in df_total.columns if col != reference_taxa]
    df_no_filter=df_total[cols]



    #Reference Taxa column
    reference_column = df_total[reference_taxa]

    info_taxa={
        'taxa-init':end_taxa-start_taxa+1,
        'zeros-deleted':0,
        'dev-mean-deleted':0,
        'remaining-taxa':end_taxa-start_taxa+1
    }

    
    if info_current_file["filter_zeros"]==None and info_current_file["filter_dev_mean"]==None:
        df_reassembled = pd.concat([df_no_filter, reference_column], axis=1)
        
    elif info_current_file["filter_zeros"]!=None and info_current_file["filter_dev_mean"]==None:
        # Only filter on zeros

        df_filtered=filter_percent_zeros(df_no_filter,info_current_file["filter_zeros"])
        info_taxa["zeros-deleted"]=info_taxa["taxa-init"]-df_filtered.shape[1]-1 # -1 for the ref column
        df_reassembled = pd.concat([df_filtered, reference_column], axis=1)
        info_taxa["remaining-taxa"]=df_reassembled.shape[1]
        
    elif info_current_file["filter_zeros"]==None and info_current_file["filter_dev_mean"]!=None:
        # Only filter on ratio dev/mean
        df_filtered=filter_deviation_mean(df_no_filter,info_current_file["filter_dev_mean"])
        info_taxa["dev-mean-deleted"]=info_taxa["taxa-init"]-df_filtered.shape[1]-1 # -1 for the ref column
        df_reassembled = pd.concat([df_filtered, reference_column], axis=1)
        info_taxa["remaining-taxa"]=df_reassembled.shape[1]
        
    elif info_current_file["filter_zeros"]!=None and info_current_file["filter_dev_mean"]!=None:
        # Two filters in the same time
        df_filtered=filter_percent_zeros(df_no_filter,info_current_file["filter_zeros"])
        info_taxa["zeros-deleted"]=info_taxa["taxa-init"]-df_filtered.shape[1]-1 # -1 for the ref column
        df_filtered=filter_deviation_mean(df_filtered,info_current_file["filter_dev_mean"])
        info_taxa["dev-mean-deleted"]=info_taxa["taxa-init"]-info_taxa["zeros-deleted"]-df_filtered.shape[1]-1 # -1 for the ref column
        df_reassembled = pd.concat([df_filtered, reference_column], axis=1)
        info_taxa["remaining-taxa"]=df_reassembled.shape[1]
    
    if type_output=="df_taxa":
        return df_reassembled
    elif type_output=="info":
        return info_taxa
    else:
        return("error")

def get_df_covariates(info_current_file,type):
    ## Type reduced or all
    start_cov=info_current_file["covar_start"]
    end_cov=info_current_file["covar_end"]
    if type=="all" or info_current_file["phenotype_column"]==None or info_current_file["phenotype_column"]=="error":
        df_before_normalization=get_df_file(info_current_file).iloc[:,start_cov-1:end_cov]
        df_normalized= (df_before_normalization - df_before_normalization.min()) / (df_before_normalization.max() - df_before_normalization.min())
        return df_normalized
    else:
        df_all_covariates=get_df_file(info_current_file).iloc[:,start_cov-1:end_cov]
        df=df_all_covariates.drop(columns=[info_current_file["phenotype_column"]])
        df_normalized= (df - df.min()) / (df.max() - df.min())
        return df_normalized

def get_infos_file(filename):
    file_extention=filename.split(".")[-1]
    if file_extention=="csv":
        df = pd.read_table(filename,sep=",")
    elif file_extention=="tsv":
        df = pd.read_table(filename,sep='\t')
    else:
        print("Error")
    num_rows, num_columns = df.shape
    return num_rows,num_columns 

def get_df_file(info_current_file):
    filename=info_current_file["filename"]
    file_extention=filename.split(".")[-1]
    if file_extention=="csv":
        df = pd.read_table(filename,sep=",")
    elif file_extention=="tsv":
        df = pd.read_table(filename,sep='\t')
    else:
        print("Error")
    return df

def get_info_separate_groups(info_current_file):

    df=get_df_file(info_current_file)
    phenotype_column=info_current_file["phenotype_column"]

    zero_count = (df[phenotype_column] == 0).sum()
    one_count = (df[phenotype_column] == 1).sum()

    return zero_count,one_count

def filter_deviation_mean(df_taxa,nb_columns):
    
    mean_values = df_taxa.mean()
    deviation_values = df_taxa.var()

    ratios=deviation_values/mean_values
    sorted_taxa = ratios.sort_values(ascending=False)
    selected_columns = sorted_taxa.head(nb_columns-1).index

    df_filtered = df_taxa[selected_columns]

    return df_filtered

def find_reference_taxa(info_current_file,reference_column=None):

    taxa_start=info_current_file["taxa_start"]
    taxa_end=info_current_file["taxa_end"]

    df=get_df_file(info_current_file)
    df_taxa=df.iloc[:,taxa_start:taxa_end+1]

    if reference_column==None:

        mean_values = df_taxa.mean()

        sorted_taxa = mean_values.sort_values(ascending=False)
        reference_column = sorted_taxa.head(1).index

        

        
        return reference_column[0]
    else:
        return df.columns[reference_column-1]
    
def filter_percent_zeros(df_taxa,percent_filtre):
    threshold = percent_filtre / 100.0 
    columns_to_keep = []


    for column in df_taxa.columns:
        zero_count = (df_taxa[column] == 0).sum()
        zero_percentage = zero_count / len(df_taxa)
        if zero_percentage <= threshold:
            columns_to_keep.append(column)

    df_filtered=df_taxa[columns_to_keep]

    return df_filtered

def get_list_taxa(info_current_file_store):
    df=get_df_taxa(info_current_file_store,"df_taxa")
    return(list(df.columns))

def get_list_covariates(info_current_file_store):
    df=get_df_covariates(info_current_file_store,"reduced")
    return (list(df.columns))

def get_list_binary_covariates(info_current_file_store):
    df=get_df_covariates(info_current_file_store,"all")
    covariate_names=list(df.columns)

    list_binary_covariates=[]

    for covariate in covariate_names:
        column = df[covariate]
        unique_values = column.unique()
        # Check whether the unique values are only 0 and 1
        if set(unique_values) == {0, 1}:
            list_binary_covariates.append(covariate)
    
    return list_binary_covariates

