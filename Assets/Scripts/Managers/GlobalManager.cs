using AIControlMagicVR.Data.Models;
using System.Collections.Generic;
using System.Threading.Tasks;
using Newtonsoft.Json;
using UnityEngine;
using System;
using TMPro;

namespace AIControlMagicVR.Managers
{
    public class GlobalManager : MonoBehaviour
    {
        public static GlobalManager Instance { get; private set; }
        public Dictionary<string, GameObject> vrStateObjects = new Dictionary<string, GameObject>();

        void Awake()
        {
            // This general VR State manager is created only once
            if (Instance != null && Instance != this)
            {
                Destroy(this.gameObject);
            }
            else
            {
                Instance = this;
            }
            Debug.Log("GlobalManager instance created.");
        }

        public void RegisterObject(GameObject obj)
        {
            // Every time a Vr State is instantiated, it is registered in the global state manager
            string universalId = Guid.NewGuid().ToString();
            if (vrStateObjects.TryAdd(universalId, obj))
            {
                Debug.Log("[GlobalManager] VR state registered. Universal Id: " + universalId);
            }
            else
            {
                Debug.Log("[GlobalManager] VR state with Universal Id: " + universalId + " already registered");
            }
        }

        public List<ObjectProperties> GetFormattedVirtualRealityState()
        {
            List<ObjectProperties> objectsProperties = new List<ObjectProperties>();
            foreach (var sceneVRState in vrStateObjects)
            {
                CoordinatesProperties position = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.position.x)
                    .Y(sceneVRState.Value.transform.position.y)
                    .Z(sceneVRState.Value.transform.position.z)
                    .build();

                CoordinatesProperties rotation = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.rotation.x)
                    .Y(sceneVRState.Value.transform.rotation.y)
                    .Z(sceneVRState.Value.transform.rotation.z)
                    .build();

                CoordinatesProperties scale = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.localScale.x)
                    .Y(sceneVRState.Value.transform.localScale.y)
                    .Z(sceneVRState.Value.transform.localScale.z)
                    .build();

                TransformProperties transform = new TransformProperties.Builder()
                    .Position(position)
                    .Rotation(rotation)
                    .Scale(scale)
                    .build();

                // Obtain the hexadecimal formatted color of the Renderer Component (e.g, #FFFFFF)
                string formattedColor = null;
                Renderer renderer = sceneVRState.Value.GetComponent<Renderer>();
                if (renderer != null){
                    formattedColor = "#" + ColorUtility.ToHtmlStringRGB(renderer.material.color);
                }

                CoordinatesProperties constantForceProps = null;
                ConstantForce constantForce = sceneVRState.Value.GetComponent<ConstantForce>();
                if (constantForce != null){
                    constantForceProps = new CoordinatesProperties.Builder()
                    .X(constantForce.force.x)
                    .Y(constantForce.force.y)
                    .Z(constantForce.force.z)
                    .build();
                }
                
                ComponentsProperties components = new ComponentsProperties.Builder()
                    .ConstantForce(constantForceProps)
                    .Color(formattedColor)
                    .build();

                ObjectProperties props = new ObjectProperties.Builder()
                    .Id(sceneVRState.Key)
                    .Tag(sceneVRState.Value.tag)
                    .Name(sceneVRState.Value.name)
                    .Components(components)
                    .Transform(transform)
                    .build();

                objectsProperties.Add(props);
            }
            Debug.Log("[GlobalManager] Completed GetFormattedVirtualRealityState()");
            return objectsProperties;
        }

        public void UpdateVRStateProperties(List<ObjectProperties> updatedVRStates)
        {
            foreach (ObjectProperties updatedVRState in updatedVRStates)
            {
                if (vrStateObjects.TryGetValue(updatedVRState.Id, out GameObject localGameObject))
                {
                    // Change color
                    Renderer renderer = localGameObject.GetComponent<Renderer>();
                    if (renderer != null)
                    {
                        Color updatedColor;
                        ColorUtility.TryParseHtmlString(updatedVRState.Components.Color, out updatedColor);

                        renderer.material.color = updatedColor;
                        Debug.Log("[Renderer] Changed color of VR State with Name: " + updatedVRState.Name + ", and ID: " + updatedVRState.Id + ", New color: " + updatedColor);
                    }
                    else
                    {
                        Debug.LogWarning("[Renderer] component not found in Name: " + updatedVRState.Name + ", and ID: " + updatedVRState.Id);
                    }

                    // Change constant force
                    ConstantForce constantForce = localGameObject.GetComponent<ConstantForce>();
                    if (constantForce != null)
                    {
                        constantForce.force = new Vector3(updatedVRState.Components.ConstantForce.X, updatedVRState.Components.ConstantForce.Y, updatedVRState.Components.ConstantForce.Z);
                        Debug.Log("[ConstantForce] Changed in Name: " + updatedVRState.Name + ", and ID: " + updatedVRState.Id + ", New Y Force: " + updatedVRState.Components.ConstantForce.Y);
                    }
                    else
                    {
                        Debug.LogWarning("[ConstantForce] component not found in Name: " + updatedVRState.Name + ", and ID: " + updatedVRState.Id);
                    }

                    // Change displayed text on television (a maximum of 539 continuous characters)
                    var tmpInputField = localGameObject.GetComponent<TextMeshProUGUI>();
                    if (tmpInputField != null)
                    {
                        tmpInputField.text = updatedVRState.Components.Text;
                        Debug.Log("[TMP_InputField] Changed in Name: " + updatedVRState.Name + ", and ID: " + updatedVRState.Id + ", New text: " + updatedVRState.Components.Text);
                    }
                    else
                    {
                        Debug.LogWarning("[TMP_InputField] component not found in Name: " + updatedVRState.Name + ", and ID: " + updatedVRState.Id);
                    }
                }
            }
        }
    }
}