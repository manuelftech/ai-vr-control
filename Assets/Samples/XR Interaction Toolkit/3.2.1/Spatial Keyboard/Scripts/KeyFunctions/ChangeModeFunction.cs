#if TEXT_MESH_PRO_PRESENT || (UGUI_2_0_PRESENT && UNITY_6000_0_OR_NEWER)
namespace UnityEngine.XR.Interaction.Toolkit.Samples.SpatialKeyboard.KeyFunctions
{
    /// <summary>
    /// Key function used to hide the keyboard.
    /// </summary>
    [CreateAssetMenu(fileName = "Change Mode Function", menuName = "XR/Spatial Keyboard/Change Mode Key Function", order = 1)]
    public class ChangeModeFunction : KeyFunction
    {
        /// <inheritdoc />
        public override void ProcessKey(XRKeyboard keyboardContext, XRKeyboardKey key)
        {
            if (keyboardContext != null){
                return;
            }
        }
    }
}

#endif


