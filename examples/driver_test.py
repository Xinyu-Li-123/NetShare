import netshare.ray as ray
from netshare import Generator

if __name__ == '__main__':
    # Change to False if you would not like to use Ray
    # ray.config.enabled = False
    ray.init(address="auto")
    # ray.init(address='10.214.96.109:10010')

    # configuration file
    # generator = Generator(config="config_example_netflow_nodp.json")
    generator = Generator(
        config="pcap/config_testpcap.json")

    # `work_folder` should not exist o/w an overwrite error will be thrown.
    # Please set the `worker_folder` as *absolute path*
    # if you are using Ray with multi-machine setup
    # since Ray has bugs when dealing with relative paths.
    generator.train_and_generate(
        work_folder='../results/pcap/testpcap')

    ray.shutdown()
