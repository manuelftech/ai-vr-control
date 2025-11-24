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
        public string ApiURL;
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
            this.GetEnvironmentVariables();
        }

        private void GetEnvironmentVariables(){
            ApiURL = Environment.GetEnvironmentVariable("VR_ENDPOINT");
            if (string.IsNullOrEmpty(ApiURL)){
                throw new System.Exception("Environment variables not found.");
            }
            Debug.Log("Environment variables successfully configured.");
        }

        public void RegisterObject(GameObject obj)
        {
            // Every time a Vr State is instantiated, it is registered in the global state manager
            string universalId = Guid.NewGuid().ToString();
            if (vrStateObjects.TryAdd(universalId, obj))
            {
                Debug.Log($"GlobalManager VR state registered. Universal Id: {universalId}");
            }
            else
            {
                Debug.Log($"GlobalManager VR state with Universal Id: {universalId} already registered.");
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
                    .Build();

                CoordinatesProperties rotation = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.rotation.x)
                    .Y(sceneVRState.Value.transform.rotation.y)
                    .Z(sceneVRState.Value.transform.rotation.z)
                    .Build();

                CoordinatesProperties scale = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.localScale.x)
                    .Y(sceneVRState.Value.transform.localScale.y)
                    .Z(sceneVRState.Value.transform.localScale.z)
                    .Build();

                TransformProperties transform = new TransformProperties.Builder()
                    .Position(position)
                    .Rotation(rotation)
                    .Scale(scale)
                    .Build();

                // Obtain the hexadecimal formatted color of the Renderer Component (e.g, #FFFFFF)
                string formattedColor = null;
                Renderer renderer = sceneVRState.Value.GetComponent<Renderer>();
                if (renderer != null){
                    formattedColor = "#" + ColorUtility.ToHtmlStringRGB(renderer.material.color);
                }

                ConstantForceProps constantForceProps = null;
                ConstantForce constantForce = sceneVRState.Value.GetComponent<ConstantForce>();
                if (constantForce != null){
                    var force = new CoordinatesProperties.Builder()
                    .X(constantForce.force.x)
                    .Y(constantForce.force.y)
                    .Z(constantForce.force.z)
                    .Build();

                    var relativeTorque = new CoordinatesProperties.Builder()
                    .X(constantForce.relativeTorque.x)
                    .Y(constantForce.relativeTorque.y)
                    .Z(constantForce.relativeTorque.z)
                    .Build();

                    constantForceProps = new ConstantForceProps.Builder()
                    .Force(force)
                    .RelativeTorque(relativeTorque)
                    .Build();
                }
                
                ComponentsProperties components = new ComponentsProperties.Builder()
                    .ConstantForce(constantForceProps)
                    .Color(formattedColor)
                    .Build();

                ObjectProperties props = new ObjectProperties.Builder()
                    .Id(sceneVRState.Key)
                    .Tag(sceneVRState.Value.tag)
                    .Name(sceneVRState.Value.name)
                    .Components(components)
                    .Transform(transform)
                    .Build();

                objectsProperties.Add(props);
            }
            Debug.Log("GlobalManager Completed formatting VR states");
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
                        Debug.Log($"Renderer: Changed color of VR State with Name: {updatedVRState.Name} and ID: {updatedVRState.Id} New color: {updatedColor}");
                    }
                    else
                    {
                        Debug.LogWarning($"Renderer component not found in Name: : {updatedVRState.Name} and ID: {updatedVRState.Id}");
                    }

                    // Change constant force
                    ConstantForce constantForce = localGameObject.GetComponent<ConstantForce>();
                    if (constantForce != null)
                    {
                        constantForce.force = new Vector3(updatedVRState.Components.ConstantForce.Force.X, updatedVRState.Components.ConstantForce.Force.Y, updatedVRState.Components.ConstantForce.Force.Z);
                        constantForce.relativeTorque = new Vector3(updatedVRState.Components.ConstantForce.RelativeTorque.X, updatedVRState.Components.ConstantForce.RelativeTorque.Y, updatedVRState.Components.ConstantForce.RelativeTorque.Z);
                        Debug.Log($"ConstantForce: Changed in Name: {updatedVRState.Name} and ID: {updatedVRState.Id}");
                    }
                    else
                    {
                        Debug.LogWarning($"ConstantForce component not found in Name: : {updatedVRState.Name} and ID: {updatedVRState.Id}");
                    }

                    // Change displayed text on television (a maximum of 539 continuous characters)
                    var tmpInputField = localGameObject.GetComponent<TextMeshPro>();
                    if (tmpInputField != null)
                    {
                        tmpInputField.text = updatedVRState.Components.Text;
                        Debug.Log($"TextMeshPro component Text Changed in Name: {updatedVRState.Name} and ID: {updatedVRState.Id} New text: {updatedVRState.Components.Text}");
                    }
                    else
                    {
                        Debug.LogWarning($"TextMeshPro component not found in Name: : {updatedVRState.Name} and ID: {updatedVRState.Id}");
                    }
                }
            }
        }
    }
}