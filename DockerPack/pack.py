# import os
import docker
import json
import argparse

client = docker.from_env()


def create_dockerfile(local_dir_name, git_url, work_dir_name, run_cmd, env_list=[],
                      base_image='python:3.6', maintainer='xlearn'):
    assert local_dir_name is not None or git_url is not None, "local and git is both None!"
    __dockerfile = ['FROM {} \n'.format(base_image),
                    'MAINTAINER {} \n'.format(maintainer)]
    for env in env_list:
        __dockerfile.append('ENV {} \n'.format(str((" ").join(env.split(",")))))
    if git_url is not None:
        __dockerfile.append('RUN git clone {} \n'.format(git_url))
    else:
        __dockerfile.append('ADD {} {} \n'.format(local_dir_name, work_dir_name), )
    __dockerfile.extend([
        'WORKDIR {} \n'.format(work_dir_name),
        'RUN pip install -r ./requirements.txt \n'.format(work_dir_name),
        # 'RUN python3 setup.py install \n',
        'CMD {}~'.format(str(run_cmd.split(",")))])
    with open("Dockerfile", 'w') as f:
        for cmd in __dockerfile:
            f.write(cmd)


def build(tag):
    return client.images.build(path='.', tag=tag)
    # os.system("docker build -t {} .".format(tag))


def show_log(log):
    for line in log:
        print(line.get("stream"))


def push(image, repo, username, password):
    if username and password:
        client.login(username=username, password=password)
    res = image.tag(repo)
    if not res:
        print("tag failed!")
        return
    else:
        client.images.push(repository=repo)
    # image_id = client.images.get(tag).short_id.replace("sha256:", "")
    # os.system("docker tag {} {}".format(image_id, repo))
    # os.system("docker push {}".format(repo))
    # client.push(repository=repo)


"""
def get_image_id(tag):
    for item in client.images():
        if tag in item["RepoTags"]:
            return (item["Id"].replace("sha256:", ""))[:12]
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


def test():
    pass


if __name__ == "__main__":
    main()
