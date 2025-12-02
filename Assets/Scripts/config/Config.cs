using System;

namespace AIControlVR.Data.Models
{
    public class Config
    {
        public static readonly string ApiURL = Environment.GetEnvironmentVariable("VR_STATE_ENDPOINT") ?? "http://localhost:5000/virtual-reality-environment/state";
        public static readonly string TextChange = Environment.GetEnvironmentVariable("TEXT_CHANGE_COMPONENT") ?? "$.Components.Text";
        public static readonly string SizeChange = Environment.GetEnvironmentVariable("SIZE_CHANGE_COMPONENT") ?? "$.Transform.Reshape";
        public static readonly string RotationChange = Environment.GetEnvironmentVariable("ROTATION_CHANGE_COMPONENT") ?? "$.Components.ConstantForce.RelativeTorque.X";
        public static readonly string LevitationChange = Environment.GetEnvironmentVariable("LEVITATION_CHANGE_COMPONENT") ?? "$.Components.ConstantForce.Force.Y";
        public static readonly string ColorChange = Environment.GetEnvironmentVariable("COLOR_CHANGE_COMPONENT") ?? "$.Components.Color";
    }
}