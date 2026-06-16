rule plot_data:
    conda:
        "envs/benchmarking.yaml"
    input:
        ha=config.hapclone_input_file,
        p=config.cnasim_reads,
        t=config.cnasim_tree
    output:
        config.data_plot
    resources:
        mem="8G"
    shell:
       "python scripts/plotting/data_plot.py -ha {input.ha} -p {input.p} -t {input.t} -o {output}"

rule plot_total:
    conda:
        "envs/benchmarking.yaml"
    input:
        ha=config.hapclone_default,
        p=config.cnasim_profiles,
        t=config.cnasim_tree
    params:
        c=config.chisel_calls_file,
        s=config.signals_output_template,
        hm=config.hmmcopy_reads_template,
    resources:
        mem="8G"
    output:
        config.total_plot
    shell:
        "python scripts/plotting/total_plots.py -ha {input.ha} -p {input.p} -t {input.t} -s {params.s} -hm {params.hm} -c {params.c} -o {output}"

rule plot_baf:
    conda:
        "envs/benchmarking.yaml"
    input:
        c=config.chisel_calls_file,
        s=config.signals_output_template,
        ha=config.hapclone_default,
        p=config.cnasim_profiles,
        t=config.cnasim_tree
    resources:
        mem="8G"
    output:
        b=config.baf_plot,
        bm=config.baf_mirror_plot
    shell:
        "python scripts/plotting/baf_plot.py -ha {input.ha} -p {input.p} -t {input.t} -s {input.s} -c {input.c} -b {output.b} -bm {output.bm}"

rule plot_hapclone_adjusted:
    conda:
        "envs/benchmarking.yaml"
    input:
        ha=config.hapclone_default,
        p=config.cnasim_profiles,
        t=config.cnasim_tree
    resources:
        mem="8G"
    output:
        b=config.hapclone_baf_adj_plot,
        tp=config.hapclone_total_adj_plot
    shell:
        "python scripts/plotting/hapclone_adj_plot.py -ha {input.ha} -p {input.p} -t {input.t} -b {output.b} -tp {output.tp}"
    
rule plot_phasing:
    conda:
        "envs/benchmarking.yaml"
    input:
        ha=config.hapclone_input_file
    output:
        p=config.phasing_plot
    resources:
        mem="8G"
    shell:
        "python scripts/plotting/phasing_plot.py -ha {input.ha} -p {output.p}"

rule plot_hapclone_baf:
    conda:
        "envs/benchmarking.yaml"
    input:
        p=config.cnasim_profiles,
        t=config.cnasim_tree,
        ha=expand(config.hapclone_results_file, hapclone_run_config=config.hapclone_cli_args, allow_missing=True)
    output:
        b=config.hapclone_baf_plot,
        bm=config.hapclone_baf_mirror_plot
    resources:
        mem="8G"
    shell:
        "python scripts/plotting/hapclone_baf_plot.py -ha {input.ha} -p {input.p} -t {input.t} -b {output.b} -bm {output.bm}"

rule plot_hapclone_total:
    conda:
        "envs/benchmarking.yaml"
    input:
        p=config.cnasim_profiles,
        t=config.cnasim_tree,
        ha=expand(config.hapclone_results_file, hapclone_run_config=config.hapclone_cli_args, allow_missing=True)
    output:
        o=config.hapclone_total_plot
    resources:
        mem="8G"
    shell:
        "python scripts/plotting/hapclone_plots.py -ha {input.ha} -p {input.p} -t {input.t} -o {output.o}"

rule plot_results:
    conda:
        "envs/benchmarking.yaml"
    input:
        p=config.ploidy_results,
        ha=config.hamming_results,
        ma=config.cluster_max_results,
        mi=config.cluster_min_results,
        b=config.cluster_between_results,
        w=config.cluster_within_results
    output:
        po=config.ploidy_plot,
        hao=config.hamming_plot,
        mio=config.min_plot,
        mao=config.max_plot,
        bo=config.between_plot,
        wo=config.within_plot
    resources:
        mem="8G"
    shell:
        "python scripts/plotting/benchmark_plot.py "
        "-p {input.p} -po {output.po} "
        "-ha {input.ha} -hao {output.hao} "
        "-ma {input.ma} -mao {output.mao} "
        "-mi {input.mi} -mio {output.mio} "
        "-b {input.b} -bo {output.bo} "
        "-w {input.w} -wo {output.wo} "

rule plot_merged_results:
    conda:
        "envs/benchmarking.yaml"
    input:
        p=expand(config.ploidy_results, sim_set=config.simulation_set_ids, allow_missing=True),
        ha=expand(config.hamming_results, sim_set=config.simulation_set_ids, allow_missing=True),
        ma=expand(config.cluster_max_results, sim_set=config.simulation_set_ids, allow_missing=True),
        mi=expand(config.cluster_min_results, sim_set=config.simulation_set_ids, allow_missing=True),
        b=expand(config.cluster_between_results, sim_set=config.simulation_set_ids, allow_missing=True),
        w=expand(config.cluster_within_results, sim_set=config.simulation_set_ids, allow_missing=True)
    output:
        ps=config.ploidy_scatter,
        pe=config.ploidy_error,
        hs=config.hamming_scatter,
        he=config.hamming_error,
        mas=config.max_scatter,
        mae=config.max_error,
        mis=config.min_scatter,
        mie=config.min_error,
        bs=config.between_scatter,
        be=config.between_error,
        ws=config.within_scatter,
        we=config.within_error
    resources:
        mem="16G"
    shell:
        "python scripts/plotting/merged_benchmark_plot.py "
        "-p {input.p} -ps {output.ps} -ps {output.pe} "
        "-ha {input.ha} -hs {output.hs} -he {output.he} "
        "-ma {input.ma} -mas {output.mas} -mae {output.mae} "
        "-mi {input.mi} -mis {output.mis} -mie {output.mie} "
        "-b {input.b} -bs {output.bs} -be {output.be} "
        "-w {intput.w} -ws {output.ws} -we {output.we} "


