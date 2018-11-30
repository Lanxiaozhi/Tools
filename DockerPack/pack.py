# import os
import docker
import argparse
import configparser

client = docker.from_env()


def create_dockerfile(info):
    print("Start create dockerfile ...")
    assert info["type"] in ["local", "git"], "Unknown pack type!"
    __dockerfile = ['FROM {} \n'.format(info["base_image"]),
                    'MAINTAINER {} \n'.format(info["maintainer"])]
    for env in info["envs"].split(";"):
        __dockerfile.append('ENV {} \n'.format(str((" ").join(env.split(",")))))
    if info["type"] == "git":
        __dockerfile.append('RUN git clone {} \n'.format(info["git_url"]))
    else:
        __dockerfile.append('ADD {} {} \n'.format(info["local_dir"], info["work_dir"]), )
    __dockerfile.extend([
        'WORKDIR {} \n'.format(info["work_dir"]),
        'RUN pip install -r ./requirements.txt \n'.format(info["work_dir"]),
        # 'RUN python3 setup.py install \n',
        'CMD {}~'.format(str(info["command"].split(",")))])
    with open("Dockerfile", 'w') as f:
        for cmd in __dockerfile:
            f.write(cmd)
    print("Create dockerfile completed!")


def build(info):
    print("Start build image ...")
    image, log = client.images.build(path='.', tag=info["image_tag"])
    if info["show_log"] == "True":
        show_log(log)
    print("Build completed!")
    return image, log
    # os.system("docker build -t {} .".format(tag))


def show_log(log):
    for line in log:
        print(line.get("stream"))


def push(info, image):
    print("Start push image ...")
    assert info["type"] in ["login_and_push", "push_only"], "Unknown push type!"
    if info["type"] == "login_and_push":
        client.login(username=info["username"], password=info["password"])
    res = image.tag(info["dockerhub_repo"])
    if not res:
        print("Tag failed!")
        return
    else:
        client.images.push(repository=info["dockerhub_repo"])
    print("Push completed!")
    # os.system("docker tag {} {}".format(image_id, repo))
    # os.system("docker push {}".format(repo))
    # client.push(repository=repo)


"""
def main():
    parse = argparse.ArgumentParser()

    parse.add_argument("-l", "--local", default=None)
    parse.add_argument("-g", "--git", default=None)
    parse.add_argument("-e", "--envs", nargs='+', default=[])
    parse.add_argument("-m", "--maintainer", default="xlearn")
    parse.add_argument("-b", "--base", default="python:3.6")
    parse.add_argument("-w", "--work")
    parse.add_argument("-t", "--tag")
    parse.add_argument("-c", "--command")

    parse.add_argument("-r", "--repo", default=None)
    parse.add_argument("-u", "--username", default=None)
    parse.add_argument("-p", "--password", default=None)

    args = parse.parse_args()

    create_dockerfile(local_dir_name=args.local, git_url=args.git, work_dir_name=args.work, run_cmd=str(args.command),
                      maintainer=args.maintainer, base_image=args.base, env_list=args.envs)
    image, log = build(tag=args.tag)
    show_log(log)
    if args.repo:
        push(image=image, repo=args.repo, username=args.username, password=args.password)
    client.close()
"""


def pack(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    dockerfile_info, build_info, push_info = {}, {}, {}
    for item in config.options("DOCKERFILE"):
        dockerfile_info[item] = config.get("DOCKERFILE", item)
    for item in config.options("BUILD"):
        build_info[item] = config.get("BUILD", item)
    for item in config.options("PUSH"):
        push_info[item] = config.get("PUSH", item)
    create_dockerfile(dockerfile_info)
    image, log = build(build_info)
    push(push_info, image)
    client.close()


def main():
    parse = argparse.ArgumentParser()

    parse.add_argument("-c", "--config")

    args = parse.parse_args()

    pack(args.config)


if __name__ == "__main__":
    main()
