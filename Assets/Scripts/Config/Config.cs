using System.Collections.Generic;
using System;

namespace AIControlVR.Configuration
{
    public class Config
    {
        public static readonly string ApiStates = Environment.GetEnvironmentVariable("VR_STATE_ENDPOINT") ?? "http://localhost:5000/virtual-reality-environment/state";
        public static readonly string ApiTextStreaming = Environment.GetEnvironmentVariable("VR_TEXT_STREAM_ENDPOINT") ?? "http://localhost:5000/virtual-reality-environment/information";
        public static readonly string TextChange = Environment.GetEnvironmentVariable("TEXT_CHANGE_COMPONENT") ?? "$.Components.Text";
        public static readonly string SizeChange = Environment.GetEnvironmentVariable("SIZE_CHANGE_COMPONENT") ?? "$.Transform.Reshape";
        public static readonly string RotationChange = Environment.GetEnvironmentVariable("ROTATION_CHANGE_COMPONENT") ?? "$.Components.ConstantForce.RelativeTorque.X";
        public static readonly string LevitationChange = Environment.GetEnvironmentVariable("LEVITATION_CHANGE_COMPONENT") ?? "$.Components.ConstantForce.Force.Y";
        public static readonly string ColorChange = Environment.GetEnvironmentVariable("COLOR_CHANGE_COMPONENT") ?? "$.Components.Color";
        public static readonly string DefaultInputTag = Environment.GetEnvironmentVariable("INPUT_TAG") ?? "keyboardText";
        public static readonly string DefaultTextDisplayTag = Environment.GetEnvironmentVariable("DEFAULT_INPUT_TAG") ?? "text";
        public static readonly string DefaultWaitingMessageSymbol = Environment.GetEnvironmentVariable("DEFAULT_WAITING_MESSAGE_SYMBOL") ?? "●";
        public static readonly string AgentLoadingMessage = Environment.GetEnvironmentVariable("AGENT_LOADING_MESSAGE") ?? "In regards to your question '{0}' let me check";
        public static readonly string StreamingTag = Environment.GetEnvironmentVariable("STREAMING_TAG") ?? "streaming_visibility";
    }
}