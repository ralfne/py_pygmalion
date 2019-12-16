import immune_receptor_utils.gene as ir_gene
import immune_receptor_utils.genes as ir_genes
from Logger import StdOutLogger
from bayesian_network_utilities.api.bayesian_network_utils import BayesianNetworkUtils
from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper
from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
from bayesian_network_utilities.api.event_merge_definition import EventMergeDefinition
from pomegranate.distributions.ConditionalProbabilityTable import ConditionalProbabilityTable
from pomegranate.distributions.DiscreteDistribution import DiscreteDistribution


class BayesianNetworkMergeUtils(object):
    @staticmethod
    def create_distribution_event_merge_definitions(gen_model_event, prefix=None, merge_singleton_events=False):
        genes = ir_genes.Genes()
        for realization in gen_model_event.realizations:
            r_name = realization.name.strip()
            gene = ir_gene.Gene(r_name, assume_01_allele=False)
            if len(gene.get_allele_text()) < 1: raise ValueError('Gene name does not contain allele')
            genes.add_gene(gene)
        unique_genes = {}
        for gene in genes:
            gene_def = gene.get_gene_text()
            unique_gene = unique_genes.get(gene_def, None)
            if unique_gene is None:
                unique_gene = ir_genes.GenePossibilities()
                unique_genes[gene_def] = unique_gene
            unique_gene.add_gene(gene, also_check_allele=True)
        merge_defs = []
        for gene_def, unique_gene in unique_genes.iteritems():
            # Singleton events (genes with one allele only) do not have to be merged; this is optional
            if len(unique_gene) > 1 or merge_singleton_events:
                merged_event_name = gene_def
                if prefix is not None:
                    merged_event_name = prefix + merged_event_name
                merge_def = EventMergeDefinition(merged_event_name)
                for g in unique_gene:
                    if prefix: s = prefix
                    s += str(g)
                    merge_def.add(s)
                merge_defs.append(merge_def)
        return merge_defs

    @staticmethod
    def create_merged_bayesian_network_for_event(event, prefix, bayesian_network, bake=False, logger=StdOutLogger(verbose=False)):
        merge_defs = BayesianNetworkMergeUtils.create_distribution_event_merge_definitions(
                                            event, prefix, merge_singleton_events=False)
        logger.log('Merging...', includeTimestamp=True)
        logger.set_carriage_reset(True)
        count = len(merge_defs)
        for index, merge_def in enumerate(merge_defs):
            logger.log("\rMerging '%s' (%i of %i)" %(merge_def.get_merged_event(), index+1, count), includeTimestamp=True)
            out = DistributionEventMergeDefinitions(event.name, bayesian_network,
                                                    allow_unspecified_events=True)
            out.set_merge_definitions([merge_def])
            bn_wrapper = BayesianNetworkWrapper(bayesian_network)
            bayesian_network = bn_wrapper.create_network_with_merged_events(out, bake=False)
        if bake: bayesian_network.bake()
        logger.set_carriage_reset(False)
        logger.log('Merging done!', includeTimestamp=True)
        return bayesian_network


    @staticmethod
    def create_merged_bayesian_network_for_events(events, prefixes, bayesian_network, bake=False, logger=StdOutLogger(verbose=False)):
        for event, prefix in zip(events, prefixes):
            bayesian_network = BayesianNetworkMergeUtils.create_merged_bayesian_network_for_event(
                                                        event, prefix, bayesian_network, bake, logger)
        return bayesian_network