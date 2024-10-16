import bpy
from . import utils
from .sd_backends.comfyui_api import (
    load_workflow,
    create_models_enum,
    create_lora_enum,
    create_control_net_enum,
    create_upscale_model_enum,
    create_comfy_sampler_enum,
    create_comfy_scheduler_enum,
    create_workflow_enum_realtime,
)

from pprint import pprint

# Colorama Placeholder
from . import Fore


LOG_PROP_CREATION = True


def create_props_from_workflow(self, context):
    """Creates the properties and add the to the comfyui_nodes collection"""

    selected_workflow_file = self.comfyui_workflow
    selected_workflow = load_workflow(context, selected_workflow_file)
    print(Fore.WHITE + "CREATING PROPERTIES FROM WORKFLOW: " + Fore.RESET + selected_workflow_file)

    set_current_workflow(self, context)

    selected_class_types = [
        "CheckpointLoaderSimple",
        "KSampler",
        "LoraLoader",
        "ControlNetApplyAdvanced",
        "ACN_AdvancedControlNetApply",
        "SelfAttentionGuidance",
        "UpscaleModelLoader",
        "CLIPSetLastLayer",
    ]

    print(Fore.WHITE + "\nSELECTED CLASS TYPE: " + Fore.RESET)
    pprint(selected_class_types)

    # Clear the comfyui_nodes collections TODO: Id possible to do it with a loop?
    self.comfyui_lora_nodes.clear()
    self.comfyui_control_net_nodes.clear()
    self.comfyui_checkpoint_loader_simple.clear()
    self.comfyui_self_attention_guidance.clear()
    self.comfyui_ksampler.clear()
    self.comfyui_upscale_model_loader.clear()
    self.comfyui_CLIP_set_last_layer.clear()

    # Update the enums
    bpy.ops.ai_render.update_ckpt_enum()
    bpy.ops.ai_render.update_lora_enum()
    bpy.ops.ai_render.update_sampler_enum()
    bpy.ops.ai_render.update_scheduler_enum()
    bpy.ops.ai_render.update_control_net_enum()
    bpy.ops.ai_render.update_upscale_model_enum()

    # Cycle through the nodes in the selected workflow and create the properties
    for node_id, node in selected_workflow.items():
        if node["class_type"] in selected_class_types:
            if node["class_type"] == "CheckpointLoaderSimple":
                if LOG_PROP_CREATION:
                    print(Fore.MAGENTA + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'Load Checkpoint'},
                    #  'class_type': 'CheckpointLoaderSimple',
                    #  'inputs': {'ckpt_name': 'SD15\\3D\\3dAnimationDiffusion_lcm.safetensors'}}

                comfyui_checkpoint_loader_simple = self.comfyui_checkpoint_loader_simple.add()
                comfyui_checkpoint_loader_simple.expanded = False
                comfyui_checkpoint_loader_simple.name = node_id
                try:
                    comfyui_checkpoint_loader_simple.ckpt_enum = node["inputs"]["ckpt_name"]
                    comfyui_checkpoint_loader_simple.ckpt_name = node["inputs"]["ckpt_name"]
                except KeyError as e:
                    print(Fore.RED + "KEY ERROR: " + Fore.RESET + e)
                    print("Check the workflow for missing keys in the node: " + node_id)
                    bpy.window_manager.popup_menu(utils.error_message, title="Error", icon="ERROR")

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_checkpoint_loader_simple.name + Fore.RESET)

            elif node["class_type"] == "LoraLoader":
                if LOG_PROP_CREATION:
                    print(Fore.YELLOW + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'Load LoRA'},
                    #  'class_type': 'LoraLoader',
                    #  'inputs': {'clip': ['28', 1],
                    #             'lora_name': 'SD15\\Robotic_Jackal-ish.safetensors',
                    #             'model': ['28', 0],
                    #             'strength_clip': 1,
                    #             'strength_model': 1}}

                comfyui_lora_node = self.comfyui_lora_nodes.add()
                comfyui_lora_node.expanded = False
                comfyui_lora_node.name = node_id
                comfyui_lora_node.strength_model = node["inputs"]["strength_model"]
                comfyui_lora_node.strength_clip = node["inputs"]["strength_clip"]
                comfyui_lora_node.lora_name = node["inputs"]["lora_name"]
                comfyui_lora_node.lora_enum = node["inputs"]["lora_name"]

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + Fore.RESET + comfyui_lora_node.name)

            elif node["class_type"] == "ControlNetApplyAdvanced":
                if LOG_PROP_CREATION:
                    print(Fore.CYAN + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'Apply ControlNet (Advanced)'},
                    #  'class_type': 'ControlNetApplyAdvanced',
                    #  'inputs': {'control_net': ['14', 0],
                    #             'end_percent': 1,
                    #             'image': ['15', 0],
                    #             'negative': ['7', 0],
                    #             'positive': ['6', 0],
                    #             'start_percent': 0,
                    #             'strength': 1}}

                # Find ControlNet model connected to the ControlNetApplyAdvanced
                control_net_node = selected_workflow[node["inputs"]["control_net"][0]]
                control_net_node_model_path = control_net_node["inputs"]["control_net_name"]

                comfyui_control_net_node = self.comfyui_control_net_nodes.add()
                comfyui_control_net_node.expanded = False
                comfyui_control_net_node.name = node_id
                comfyui_control_net_node.strength = node["inputs"]["strength"]
                comfyui_control_net_node.start_percent = node["inputs"]["start_percent"]
                comfyui_control_net_node.end_percent = node["inputs"]["end_percent"]
                comfyui_control_net_node.control_net_name = control_net_node_model_path
                comfyui_control_net_node.control_net_enum = control_net_node_model_path

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_control_net_node.name + Fore.RESET)

            elif node["class_type"] == "ACN_AdvancedControlNetApply":
                if LOG_PROP_CREATION:
                    print(Fore.CYAN + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'Apply Advanced ControlNet 🛂🅐🅒🅝'},
                    #  'class_type': 'ACN_AdvancedControlNetApply',
                    #  'inputs': {'control_net': ['85', 0],
                    #             'end_percent': 0.5,
                    #             'image': ['18', 0],
                    #             'model_optional': ['37', 0],
                    #             'negative': ['13', 1],
                    #             'positive': ['13', 0],
                    #             'start_percent': 0,
                    #             'strength': 0.5}}

                # Find ControlNet model connected to the ACN_AdvancedControlNetApply
                control_net_node = selected_workflow[node["inputs"]["control_net"][0]]
                control_net_node_model_path = control_net_node["inputs"]["control_net_name"]

                comfyui_acn_advanced_control_net_apply = self.comfyui_acn_advanced_control_net_apply.add()
                comfyui_acn_advanced_control_net_apply.expanded = False
                comfyui_acn_advanced_control_net_apply.name = node_id
                comfyui_acn_advanced_control_net_apply.strength = node["inputs"]["strength"]
                comfyui_acn_advanced_control_net_apply.start_percent = node["inputs"]["start_percent"]
                comfyui_acn_advanced_control_net_apply.end_percent = node["inputs"]["end_percent"]
                comfyui_acn_advanced_control_net_apply.control_net_name = control_net_node_model_path
                comfyui_acn_advanced_control_net_apply.control_net_enum = control_net_node_model_path

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_acn_advanced_control_net_apply.name + Fore.RESET)

            elif node["class_type"] == "SelfAttentionGuidance":
                if LOG_PROP_CREATION:
                    print(Fore.BLUE + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'Self-Attention Guidance'},
                    #  'class_type': 'SelfAttentionGuidance',
                    #  'inputs': {'blur_sigma': 2, 'model': ['26', 0], 'scale': 1}}

                comfyui_self_attention_guidance = self.comfyui_self_attention_guidance.add()
                comfyui_self_attention_guidance.expanded = False
                comfyui_self_attention_guidance.name = node_id
                comfyui_self_attention_guidance.blur_sigma = node["inputs"]["blur_sigma"]
                comfyui_self_attention_guidance.scale = node["inputs"]["scale"]

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_self_attention_guidance.name + Fore.RESET)

            elif node["class_type"] == "KSampler":
                if LOG_PROP_CREATION:
                    print(Fore.GREEN + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'main_sampler'},
                    #  'class_type': 'KSampler',
                    #  'inputs': {'cfg': 7.5,
                    #             'denoise': 1,
                    #             'latent_image': ['10', 0],
                    #             'model': ['37', 0],
                    #             'negative': ['16', 1],
                    #             'positive': ['16', 0],
                    #             'sampler_name': 'dpmpp_2m_sde_gpu',
                    #             'scheduler': 'karras',
                    #             'seed': 967975925929612,
                    #             'steps': 10}}

                comfyui_ksampler = self.comfyui_ksampler.add()

                if node["_meta"]["title"] == "main_sampler":
                    comfyui_ksampler.is_main_sampler = True

                comfyui_ksampler.expanded = False
                comfyui_ksampler.name = node_id
                trimmed_seed = node["inputs"]["seed"] % 1000000000
                comfyui_ksampler.seed = trimmed_seed
                comfyui_ksampler.steps = node["inputs"]["steps"]
                comfyui_ksampler.cfg = node["inputs"]["cfg"]
                comfyui_ksampler.sampler_name = node["inputs"]["sampler_name"]
                comfyui_ksampler.sampler_enum = node["inputs"]["sampler_name"]
                comfyui_ksampler.scheduler_name = node["inputs"]["scheduler"]
                comfyui_ksampler.scheduler_enum = node["inputs"]["scheduler"]

                comfyui_ksampler.denoise = node["inputs"]["denoise"]

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_ksampler.name + Fore.RESET)

            elif node["class_type"] == "UpscaleModelLoader":
                if LOG_PROP_CREATION:
                    print(Fore.RED + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'Load Upscale Model'},
                    #  'class_type': 'UpscaleModelLoader',
                    #  'inputs': {'model_name': '4x-UltraSharp.pth'}}

                comfyui_upscale_model_loader = self.comfyui_upscale_model_loader.add()
                comfyui_upscale_model_loader.expanded = False
                comfyui_upscale_model_loader.name = node_id
                comfyui_upscale_model_loader.upscale_model_name = node["inputs"]["model_name"]
                comfyui_upscale_model_loader.upscale_model_enum = node["inputs"]["model_name"]

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_upscale_model_loader.name + Fore.RESET)

            elif node["class_type"] == "CLIPSetLastLayer":
                if LOG_PROP_CREATION:
                    print(Fore.MAGENTA + "\nNODE: " + node_id)
                    pprint(node)
                    # {'_meta': {'title': 'CLIP Set Last Layer'},
                    # 'class_type': 'CLIPSetLastLayer',
                    # 'inputs': {'clip': ['4', 1], 'stop_at_clip_layer': -24}}

                comfyui_clip_set_last_layer = self.comfyui_CLIP_set_last_layer.add()
                comfyui_clip_set_last_layer.name = node_id
                comfyui_clip_set_last_layer.expanded = False
                comfyui_clip_set_last_layer.stop_at_clip_layer = node["inputs"]["stop_at_clip_layer"]

                if LOG_PROP_CREATION:
                    print(Fore.WHITE + "PROPERTIES CREATED FOR NODE: " + comfyui_clip_set_last_layer.name + Fore.RESET)


def set_current_workflow(self, context):
    self.comfy_current_workflow = self.comfyui_workflow


def set_ckpt_name(self, context):
    self.ckpt_name = self.ckpt_enum


def set_lora_name(self, context):
    self.lora_name = self.lora_enum


def set_upscale_model_name(self, context):
    self.upscale_model_name = self.upscale_model_enum


def set_comfy_sampler_name(self, context):
    self.sampler_name = self.sampler_enum


def set_comfy_scheduler_name(self, context):
    self.scheduler_name = self.scheduler_enum


class ComfyUICheckpointLoaderSimple(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    ckpt_name: bpy.props.StringProperty(name="ckpt_name", default="", description="Name of the checkpoint model")
    ckpt_enum: bpy.props.EnumProperty(name="ckpt_enum", default=0, items=create_models_enum, description="A list of the available checkpoints", update=set_ckpt_name)


class ComfyUILoraNode(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    lora_name: bpy.props.StringProperty(name="current_lora_model", default="", description="Name of the LoRA model")
    lora_enum: bpy.props.EnumProperty(name="lora_enum", default=0, items=create_lora_enum, description="A list of the available LoRA models", update=set_lora_name)
    strength_model: bpy.props.FloatProperty(name="Lora Model Strength", default=1, soft_min=0, soft_max=1, min=0, max=10, description="Strength of the LoRA model")
    strength_clip: bpy.props.FloatProperty(name="Lora Clip Strength", default=1, soft_min=0, soft_max=1, min=0, max=10, description="Strength of the CLIP model")


class ComfyUIControlNetNode(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    control_net_name: bpy.props.StringProperty(name="ControlNet Name", default="", description="Name of the ControlNet model")
    control_net_enum: bpy.props.EnumProperty(name="control_net_enum", default=0, items=create_control_net_enum, description="A list of the available ControlNet models")
    strength: bpy.props.FloatProperty(
        name="ControlNet Strength",
        default=1,
        soft_min=0,
        soft_max=1,
        min=0,
        max=10,
        description="Strength of the ControlNet model",
    )
    start_percent: bpy.props.FloatProperty(name="ControlNet Start Percent", default=0, min=0, max=1, description="Start percent of the ControlNet model")
    end_percent: bpy.props.FloatProperty(name="ControlNet End Percent", default=1, min=0, max=1, description="End percent of the ControlNet model")


class ComfyUIACNAdvancedControlNetApply(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    control_net_name: bpy.props.StringProperty(name="ControlNet Name", default="", description="Name of the ControlNet model")
    control_net_enum: bpy.props.EnumProperty(name="control_net_enum", default=0, items=create_control_net_enum, description="A list of the available ControlNet models")
    strength: bpy.props.FloatProperty(
        name="ControlNet Strength",
        default=1,
        soft_min=0,
        soft_max=1,
        min=0,
        max=10,
        description="Strength of the ControlNet model",
    )
    start_percent: bpy.props.FloatProperty(name="ControlNet Start Percent", default=0, min=0, max=1, description="Start percent of the ControlNet model")
    end_percent: bpy.props.FloatProperty(name="ControlNet End Percent", default=1, min=0, max=1, description="End percent of the ControlNet model")


class ComfyUIUpscaleModelLoader(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    upscale_model_name: bpy.props.StringProperty(name="upscale_model_name", default="", description="Name of the upscale model")
    upscale_model_enum: bpy.props.EnumProperty(
        name="upscale_model_enum", default=0, items=create_upscale_model_enum, description="A list of the available upscale models", update=set_upscale_model_name
    )


class ComfyUISelfAttentionGuidance(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    blur_sigma: bpy.props.FloatProperty(name="Self-Attention Guidance Blur Sigma", default=2, soft_min=0, soft_max=10, min=0, max=10, description="Blur sigma")
    scale: bpy.props.FloatProperty(name="Self-Attention Guidance Scale", default=0.5, min=-2, max=5, description="Scale")


class ComfyUIMainKSampler(bpy.types.PropertyGroup):
    # """This should map only with the main_sampler node in the workflow"""

    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    seed: bpy.props.IntProperty(
        name="Seed",
        min=0,
        description="Seed",
    )
    is_main_sampler: bpy.props.BoolProperty(name="is_main_sampler", default=False, description="Is the Main Sampler connected to Save Image")
    steps: bpy.props.IntProperty(
        name="Steps",
        default=10,
        soft_min=1,
        soft_max=50,
        min=1,
        max=150,
        description="Steps",
    )
    cfg: bpy.props.FloatProperty(
        name="Cfg",
        default=7,
        soft_min=1,
        soft_max=24,
        min=0,
        max=35,
        description="Cfg",
    )
    sampler_name: bpy.props.StringProperty(name="current_sampler_name", default="", description="Name of the sampler")
    sampler_enum: bpy.props.EnumProperty(name="sampler_enum", default=130, items=create_comfy_sampler_enum, description="A list of the available samplers", update=set_comfy_sampler_name)
    scheduler_name: bpy.props.StringProperty(name="current_scheduler_name", default="", description="Name of the scheduler")
    scheduler_enum: bpy.props.EnumProperty(name="scheduler_enum", default=20, items=create_comfy_scheduler_enum, description="A list of the available schedulers", update=set_comfy_scheduler_name)
    denoise: bpy.props.FloatProperty(
        name="Denoise",
        default=0.8,
        description="Denoise",
        min=0.001,
        max=1,
    )


class ComfyUICLIPSetLastLayer(bpy.types.PropertyGroup):
    expanded: bpy.props.BoolProperty(name="expanded", default=True, description="Expanded")
    stop_at_clip_layer: bpy.props.IntProperty(name="stop_at_clip_layer", default=-1, min=-24, max=-1, description="Stop at Clip Layer")


class ComfyUIProps(bpy.types.PropertyGroup):
    comfy_current_workflow: bpy.props.StringProperty(
        name="comfyui_current_workflow",
        default="",
        description="Current workflow",
    )
    comfyui_workflow: bpy.props.EnumProperty(
        name="comfyui_workflow",
        default=0,
        items=create_workflow_enum_realtime,
        description="A list of the available workflows in the path specified in the addon preferences",
        update=create_props_from_workflow,
    )
    comfyui_checkpoint_loader_simple: bpy.props.CollectionProperty(type=ComfyUICheckpointLoaderSimple)
    comfyui_ksampler: bpy.props.CollectionProperty(type=ComfyUIMainKSampler)
    comfyui_lora_nodes: bpy.props.CollectionProperty(type=ComfyUILoraNode)
    comfyui_control_net_nodes: bpy.props.CollectionProperty(type=ComfyUIControlNetNode)
    comfyui_acn_advanced_control_net_apply: bpy.props.CollectionProperty(type=ComfyUIACNAdvancedControlNetApply)
    comfyui_self_attention_guidance: bpy.props.CollectionProperty(type=ComfyUISelfAttentionGuidance)
    comfyui_upscale_model_loader: bpy.props.CollectionProperty(type=ComfyUIUpscaleModelLoader)
    comfyui_CLIP_set_last_layer: bpy.props.CollectionProperty(type=ComfyUICLIPSetLastLayer)


classes = [
    ComfyUICheckpointLoaderSimple,
    ComfyUIMainKSampler,
    ComfyUILoraNode,
    ComfyUIControlNetNode,
    ComfyUIACNAdvancedControlNetApply,
    ComfyUISelfAttentionGuidance,
    ComfyUIUpscaleModelLoader,
    ComfyUICLIPSetLastLayer,
    ComfyUIProps,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.comfyui_props = bpy.props.PointerProperty(type=ComfyUIProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.comfyui_props
