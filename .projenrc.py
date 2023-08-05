from projen.python import PythonProject

project = PythonProject(
    author_email="mike@graywind.org",
    author_name="Mike Gray",
    module_name="skill_mark2_audio_receiver",
    name="skill-mark2-audio-receiver",
    version="0.1.0",
)

project.synth()