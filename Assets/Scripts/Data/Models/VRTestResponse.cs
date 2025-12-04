using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class VRTextResponse
    {
        public string Text;
        
        public VRTextResponse() { }
        public class Builder
        {
            private VRTextResponse _build = new VRTextResponse();
            public Builder Text(string text)
            {
                 _build.Text = text;
                 return this;
            }
            public VRTextResponse Build()
            {
                return _build;
            }
        }
    }
}