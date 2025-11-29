using AIControlVR.Managers.Networking;
using System.Collections.Generic;
using AIControlVR.Data.Models;
using System.Threading.Tasks;
using Newtonsoft.Json;
using UnityEngine;
using System;
using TMPro;

namespace AIControlVR.Managers
{
    public class GlobalManager : MonoBehaviour
    {
        public string ApiURL;
        public static GlobalManager Instance { get; private set; }
        private APIVRProperties apiVRProperties = new APIVRProperties();
        public Dictionary<string, GameObject> vrStateObjects = new Dictionary<string, GameObject>();

        async void Awake()
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

            // Run the following function 10 seconds after loading the 3D environment
            await this.SaveInitialStatusToRedis();
        }

        private async Task SaveInitialStatusToRedis(){
            await Task.Delay(13000);
            // Send the initial 3D VR status to Redis
            await apiVRProperties.SaveInitialVrStatus(this.GetFormattedVirtualRealityState());
            Debug.Log("Initial status successfully saved to Redis.");
        }

        private void GetEnvironmentVariables(){
            ApiURL = Environment.GetEnvironmentVariable("VR_STATE_ENDPOINT") ?? "http://localhost:5000/virtual-reality-environment/state";
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
                    formattedColor = $"#{ColorUtility.ToHtmlStringRGB(renderer.material.color)}";
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

        public void UpdateVRStateProperties(VRStateResponse updatedVRStates)
        {
            foreach (var sceneVRState in vrStateObjects)
            {
                if (!sceneVRState.Value.tag.Contains(updatedVRStates.Tag, StringComparison.OrdinalIgnoreCase)){
                    continue;
                }
                Renderer renderer = sceneVRState.Value.GetComponent<Renderer>();
                ConstantForce constantForce = sceneVRState.Value.GetComponent<ConstantForce>();
                foreach (VRProperty vr in updatedVRStates.Properties){
                    switch(vr.Name){
                        case "$.Components.Color":
                            // Modifies the color of the element
                            if (renderer){
                                Color updatedColor;
                                ColorUtility.TryParseHtmlString(vr.State, out updatedColor);
                                renderer.material.color = updatedColor;
                                Debug.Log($"Tag: {updatedVRStates.Tag}. Color assigned: {vr.State}");
                            }
                            continue;
                        case "$.Components.ConstantForce.Force.Y":
                            // Modifies the gravity of the element
                            if (constantForce){
                                Vector3 updatedForce = constantForce.force;
                                updatedForce.y = float.Parse(vr.State);
                                constantForce.force = updatedForce;
                            }
                            Debug.Log($"Tag: {updatedVRStates.Tag}. ConstantForce.Force assigned: {vr.State}");
                            continue;
                        case "$.Components.ConstantForce.RelativeTorque.X":
                            // Modifies the spinning force of the element
                            if (constantForce){
                                Vector3 updatedTorque = constantForce.relativeTorque;
                                updatedTorque.x = float.Parse(vr.State);
                                constantForce.relativeTorque = updatedTorque;
                            }
                            Debug.Log($"Tag: {updatedVRStates.Tag}. ConstantForce.RelativeTorque assigned: {vr.State}");
                            continue;
                        case "$.Transform.Scale":
                            // Modifies the size of the element
                            Vector3 scale = sceneVRState.Value.transform.localScale;
                            scale.x = scale.x * float.Parse(vr.State);
                            scale.y = scale.y * float.Parse(vr.State);
                            scale.z = scale.z * float.Parse(vr.State);
                            sceneVRState.Value.transform.localScale = scale;
                            Debug.Log($"Tag: {updatedVRStates.Tag}. Transform.Scale assigned: {vr.State}");
                            continue;
                    }
                }
            }
            Debug.Log("VR environment Successfully modified");
        }
    }
}