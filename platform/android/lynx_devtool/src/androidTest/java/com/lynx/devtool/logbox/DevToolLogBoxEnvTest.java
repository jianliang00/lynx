// Copyright 2025 The Lynx Authors. All rights reserved.
// Licensed under the Apache License Version 2.0 that can be found in the
// LICENSE file in the root directory of this source tree.
package com.lynx.devtool.logbox;

import static org.junit.Assert.*;

import android.content.Context;
import org.junit.Before;
import org.junit.Test;

public class DevToolLogBoxEnvTest {
  private Boolean mFlag;

  @Before
  public void setUp() {
    mFlag = false;
  }

  @Test
  public void registerErrorParserLoader() {
    DevToolLogBoxEnv.ILogBoxErrorParserLoader loader =
        new DevToolLogBoxEnv.ILogBoxErrorParserLoader() {
          @Override
          public void loadErrorParser(Context context, DevToolLogBoxCallback callback) {
            mFlag = true;
            callback.onSuccess("test data");
            callback.onFailure("test error");
          }
        };
    DevToolLogBoxEnv.inst().registerErrorParserLoader("register-test", loader);
    DevToolLogBoxEnv.inst().loadErrorParser(null, "register-test", new DevToolLogBoxCallback() {
      @Override
      public void onSuccess(String data) {
        assertEquals(data, "test data");
      }

      @Override
      public void onFailure(String reason) {
        assertEquals(reason, "test error");
      }
    });
    assertTrue(mFlag);
  }
}
