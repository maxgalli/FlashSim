import dask.dataframe as dd
from dask.distributed import LocalCluster, Client
import matplotlib.pyplot as plt
import os

def plot_var(df, var, output_dir):
    fig, ax = plt.subplots()
    ax.hist(df[var], bins=100, histtype="step")
    for ext in ["png", "pdf"]:
        fig.savefig(os.path.join(output_dir, f"preprocess_{var}.{ext}"))

def main():
    file_path_pattern = '/work/gallim/SIMStudies/FlashSim/out/photons/*.parquet'
    output_dir = "/eos/home-g/gallim/www/plots/SIMStudies/FlashSim/tries"
    
    # start a local cluster for parallel processing
    cluster = LocalCluster()
    client = Client(cluster)
   
    print("Reading files...")
    df = dd.read_parquet(file_path_pattern, engine='fastparquet')
    df = df.compute()
    
    for var in df.columns:
        print(f"Plotting {var}...")
        plot_var(df, var, output_dir)

    # close the local cluster
    client.close()
    cluster.close()

if __name__ == '__main__':
    main()